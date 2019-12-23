from enum import Enum
import ipaddress
from marshmallow import fields, Schema, ValidationError
from marshmallow_enum import EnumField
from flask_rebar import RequestSchema


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
    cluster_id = fields.UUID(required=True)


class HypervisorSchema(Schema):
    id = fields.UUID()
    cluster_id = fields.UUID()
    status = EnumField(ClusterStatus)
    ip_address = fields.String(validate=validate_ip)
