from marshmallow import Schema, fields
from agent.src.schema.accelerometer_schema import AccelerometerSchema
from agent.src.schema.gps_schema import GpsSchema
from agent.src.domain.aggregated_data import AggregatedData


class AggregatedDataSchema(Schema):
    accelerometer = fields.Nested(AccelerometerSchema)
    gps = fields.Nested(GpsSchema)
    time = fields.DateTime('iso')
