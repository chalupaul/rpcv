from uuid import UUID

import flask_rebar
from flask_rebar import errors

from rpcv.app import registry
from rpcv.schemas.hypervisor import HypervisorSchema, CreateHypervisorSchema


@registry.handles(
    rule="/hypervisors", method="POST", request_body_schema=CreateHypervisorSchema(),
)
def create_hypervisor():
    body = flask_rebar.get_validated_body()
    account = body
    return account, 201


@registry.handles(
    rule="/hypervisors/<uuid:hypervisor_uuid>",
    method="GET",
    query_string_schema=CreateHypervisorSchema(),
)
def get_hypervisor(hypervisor_uuid: UUID):
    hypervisor = HypervisorSchema()
    if hypervisor is None:
        raise errors.NotFound()

    return hypervisor.uuid


@registry.handles(
    rule="/hypervisors/<uuid:hypervisor_uuid>",
    method="PATCH",
    request_body_schema=CreateHypervisorSchema(),
)
def update_hypervisor(hypervisor_uuid: UUID):
    body = flask_rebar.get_validated_body()

    hypervisor = body
    if hypervisor is None:
        raise errors.NotFound()

    return "", 204


@registry.handles(rule="/hypervisors/<uuid:cluster_uuid>", method="DELETE")
def delete_hypervisor(account_uuid: UUID):
    hypervisor = {}
    if hypervisor is None:
        raise errors.NotFound()

    return "", 204
