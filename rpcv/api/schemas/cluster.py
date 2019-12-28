from enum import Enum

from flask_rebar import RequestSchema
from marshmallow import Schema, fields
from marshmallow_enum import EnumField


class ClusterStatus(Enum):
    CREATING = 1
    ONLINE = 2
    DEGRADED = 3
    ERROR = 4


class CreateClusterSchema(RequestSchema):
    pass


class ClusterSchema(Schema):
    uuid = fields.UUID()
    status = EnumField(ClusterStatus)
    hypervisors = fields.List(fields.UUID())
    created_at = fields.DateTime()
