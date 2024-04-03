from dataclasses import dataclass
from datetime import datetime
from agent.src.domain.accelerometer import Accelerometer
from agent.src.domain.gps import Gps


@dataclass
class AggregatedData:
    accelerometer: Accelerometer
    gps: Gps
    time: datetime
