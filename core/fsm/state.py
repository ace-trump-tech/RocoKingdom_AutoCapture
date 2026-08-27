# core/fsm/state.py
from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    SEARCHING = auto()
    TRACKING = auto()
    THROWING = auto()
    COMBAT = auto()
    COLLECTING_GEM = auto()
    BUYING_BALLS = auto()
    PAUSE = auto()
    EXIT = auto()
