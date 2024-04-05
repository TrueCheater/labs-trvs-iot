from dataclasses import dataclass
from datetime import datetime


@dataclass
class Gps:
    longitude: float
    latitude: float
    time: datetime
