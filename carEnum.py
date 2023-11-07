from enum import Enum

class CarOperation(Enum):
    ACCEL = "accel"
    DECEL = "decel"
    CLOSE = "close"
    LANE_LEFT = "l"
    LANE_RIGHT = "r"
    OK = "OK"
