from uuid import UUID

import flask_rebar
from flask_rebar import errors

from ..app.server import registry
from ..schemas.cluster import ClusterSchema, CreateClusterSchema, ClusterStatus

from typing import Dict, Tuple, Any


@registry.handles(
    rule="/clusters", method="POST", request_body_schema=CreateClusterSchema(),
)
def create_cluster() -> Tuple[Dict[str, Any], int]:
    body = flask_rebar.get_validated_body()
    sample_data = {
        "uuid": body.uuid,
        "status": "CREATING",
        "hypervisors": [],
    }

    cluster: Dict[str, Any] = ClusterSchema().dumps(sample_data)
    return cluster, 201


@registry.handles(
    rule="/clusters/<uuid:cluster_uuid>",
    method="GET",
    query_string_schema=CreateClusterSchema(),
)
def get_cluster(cluster_uuid: UUID) -> Dict[str, Any]:
    sample_data = {
        "uuid": cluster_uuid,
        "status": getattr(ClusterStatus, "CREATING"),
        "hypervisors": [],
    }

    cluster: Dict[str, Any] = ClusterSchema().dumps(sample_data)
    if cluster is None:
        raise errors.NotFound()

    return cluster


@registry.handles(
    rule="/clusters/<uuid:cluster_uuid>",
    method="PATCH",
    request_body_schema=CreateClusterSchema(),
)
def update_cluster(cluster_uuid: UUID) -> Tuple[str, int]:
    body = flask_rebar.get_validated_body()

    cluster = body
    if cluster is None:
        raise errors.NotFound()

    return "", 204


@registry.handles(rule="/clusters/<uuid:cluster_uuid>", method="DELETE")
def delete_cluster(cluster_uuid: UUID) -> Tuple[str, int]:
    cluster: Dict[str, Any] = {}
    if cluster is None:
        raise errors.NotFound()

    return "", 204
