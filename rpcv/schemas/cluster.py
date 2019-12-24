from enum import Enum
from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from flask_rebar import RequestSchema


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
