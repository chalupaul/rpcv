from uuid import UUID

import flask_rebar
from flask_rebar import errors

from ..app.server import registry
from ..schemas.hypervisor import HypervisorSchema, CreateHypervisorSchema
from typing import Dict, Tuple, Any


@registry.handles(
    rule="/hypervisors", method="POST", request_body_schema=CreateHypervisorSchema(),
)
def create_hypervisor() -> Tuple[Dict[str, Any], int]:
    body = flask_rebar.get_validated_body()
    account = body
    return {"new": account}, 201


@registry.handles(
    rule="/hypervisors/<uuid:hypervisor_uuid>",
    method="GET",
    query_string_schema=CreateHypervisorSchema(),
)
def get_hypervisor(hypervisor_uuid: UUID) -> Any:
    hypervisor = HypervisorSchema()
    if hypervisor is None:
        raise errors.NotFound()

    return hypervisor.uuid


@registry.handles(
    rule="/hypervisors/<uuid:hypervisor_uuid>",
    method="PATCH",
    request_body_schema=CreateHypervisorSchema(),
)
def update_hypervisor(hypervisor_uuid: UUID) -> Tuple[str, int]:
    body = flask_rebar.get_validated_body()

    hypervisor = body
    if hypervisor is None:
        raise errors.NotFound()

    return "", 204


@registry.handles(rule="/hypervisors/<uuid:cluster_uuid>", method="DELETE")
def delete_hypervisor(hypervisor_uuid: UUID) -> Tuple[str, int]:
    hypervisor: Dict[str, str] = {}
    if hypervisor is None:
        raise errors.NotFound()

    return "", 204
