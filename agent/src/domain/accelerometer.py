from dataclasses import dataclass
from datetime import datetime


@dataclass
class Accelerometer:
    x: int
    y: int
    z: int
    time: datetime
