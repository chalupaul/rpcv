import ipaddress
from enum import Enum

from flask_rebar import RequestSchema
from marshmallow import Schema, ValidationError, fields
from marshmallow_enum import EnumField


class ClusterStatus(Enum):
    AWAITING_CALLBACK = 1
    CONFIGURING = 2
    ONLINE = 3
    DEGRADED = 4
    ERROR = 5


def validate_ip(ip: str) -> None:
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValidationError("Invalid IP address.")


class CreateHypervisorSchema(RequestSchema):
    cluster_uuid = fields.UUID(required=True)


class HypervisorSchema(Schema):
    uuid = fields.UUID()
    cluster_uuid = fields.UUID()
    status = EnumField(ClusterStatus)
    ip_address = fields.String(validate=validate_ip)
