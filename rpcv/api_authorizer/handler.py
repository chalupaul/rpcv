import copy
import json
import requests
from typing import Any, Dict

import rpcv.common.log
from authpolicy import AuthPolicy

logger = rpcv.common.log.get_logger()


def build_policy(method_arn: str, user_id: str, allow: bool = False) -> Any:
    """Create API Gateway policy."""
    if allow:
        # example of methodArn:
        # arn:aws:execute-api:<Region id>:<Account id>:<API id>/
        # <Stage>/<Method>/<Resource path>
        tmp = method_arn.split(":")
        api_gateway_arn = tmp[5].split("/")
        aws_account_id = tmp[4]
        method = api_gateway_arn[2]
        resource = "/".join(api_gateway_arn[3:])
        principalId = f"user|{user_id}"

        # Build the authorizer policy
        policy = AuthPolicy(principalId, aws_account_id)
        policy.allowMethod(method, resource)
        response = policy.build()
        logger.info("Returning normal response", http_status=200)
        return response
    else:
        # Token was invalid, time to reject with a 401.
        # Custom authorizer can only return either policies (allow - 200 or
        # deny - 403), or `Unauthorized` exceptions. Anything else and the
        # client receives a 500 error.
        logger.exception("Unauthorized request", http_status=401)
        raise Exception("Unauthorized")


def setup_handler(event: Dict[str, Any], context: Dict[str, Any]) -> None:
    """Setup request object and bind to logger for debugging."""
    logger.debug(event)

    # Parse the request from the event.
    request = {}
    request["methodArn"] = event["methodArn"]
    request["type"] = event["type"]
    request["token"] = event["authorizationToken"]
    log_request = copy.deepcopy(request)

    # Don't log the whole token.
    log_request["token"] = event["authorizationToken"][-8:]

    # Bind the request info to the logger. You may want to filter
    # request['token'] so as not to log it like the example above.
    logger.bind(request_context=log_request)


def verify_rackspace_identity(token: str) -> requests.Response:
    """Call Rackspace Identity and verify provided token."""
    url = "https://heimdall.api.manage.rackspace.com/v2.0/tokens/{}"
    headers = {"X-Auth-Token": token}

    # This will use the retries/timeouts configured above.
    return requests.get(url.format(token), headers=headers)


def is_racker(identity_response: Dict[str, Any]) -> bool:
    """Examine roles and return True if Racker role present."""
    roles = identity_response.get("access", {}).get("user", {}).get("roles", [])
    for role in roles:
        if role.get("name") == "Racker" and role.get("id") == "9":
            return True
    return False


def rackspace_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Any:
    """Entrypoint for Rackspace Identity authorizer."""
    setup_handler(event, context)
    logger.info("Authorizing via Rackspace Identity ...")

    response = verify_rackspace_identity(event["token"])
    allow = True if response.ok else False

    if not allow:
        logger.info(
            "Error verifying Rackspace identity",
            status_code=response.status_code,
            response=response.text,
        )

    identity = response.json()
    user_id = identity.get("access", {}).get("user", {}).get("id", None)
    policy = build_policy(event["methodArn"], user_id, allow=allow)
    # Add Rackspace Identity context
    policy["context"] = {
        "domainId": identity["access"]["user"].get("RAX-AUTH:domainId"),
        "name": identity["access"]["user"]["name"],
        "userId": identity["access"]["user"]["id"],
        "racker": is_racker(identity),
        "access": json.dumps(identity),
    }
    return policy
