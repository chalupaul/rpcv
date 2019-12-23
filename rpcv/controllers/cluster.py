from uuid import UUID

import flask_rebar
from flask_rebar import errors

from rpcv.app import registry
from rpcv.schemas.cluster import ClusterSchema, CreateClusterSchema, ClusterStatus


@registry.handles(
    rule="/clusters", method="POST", request_body_schema=CreateClusterSchema(),
)
def create_cluster():
    body = flask_rebar.get_validated_body()
    sample_data = {
        "id": body.id,
        "status": "CREATING",
        "hypervisors": [],
    }

    cluster = ClusterSchema().dumps(sample_data)
    return cluster, 201


@registry.handles(
    rule="/clusters/<uuid:cluster_id>",
    method="GET",
    query_string_schema=CreateClusterSchema(),
)
def get_cluster(cluster_id: UUID):
    sample_data = {
        "id": cluster_id,
        "status": getattr(ClusterStatus, "CREATING"),
        "hypervisors": [],
    }

    cluster = ClusterSchema().dumps(sample_data)
    if cluster is None:
        raise errors.NotFound()

    return cluster


@registry.handles(
    rule="/clusters/<uuid:cluster_id>",
    method="PATCH",
    request_body_schema=CreateClusterSchema(),
)
def update_cluster(cluster_id: UUID):
    body = flask_rebar.get_validated_body()

    cluster = body
    if cluster is None:
        raise errors.NotFound()

    return "", 204


@registry.handles(rule="/clusters/<uuid:cluster_id>", method="DELETE")
def delete_cluster(cluster_id: UUID):
    cluster = {}
    if cluster is None:
        raise errors.NotFound()

    return "", 204
