from marshmallow import Schema, fields
from agent.src.domain.accelerometer import Accelerometer


class AccelerometerSchema(Schema):
    x = fields.Int()
    y = fields.Int()
    z = fields.Int()
