from enum import Enum

class CarOperation(Enum):
    ACCEL = "accel"
    DECEL = "decel"
    CLOSE = "close"
    LANE_LEFT = "lane_left"
    LANE_RIGHT = "lane_right"
    OK = "OK"
