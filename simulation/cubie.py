from enum import Enum
import copy

class CubieType(Enum):
    EDGE = 0
    CORNER = 1
    CENTER = 2

class FaceOrientation(Enum):
    UP = 0
    LEFT = 1
    FRONT = 2
    RIGHT = 3
    BACK = 4
    DOWN = 5

class CubiePosition:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

    def __eq__(self, other):
        return self.position  == other.position and self.orientation == other.orientation

class Cubie:
    def __init__(self, cubie_type, cubie_colors, correct_position):
        self.type = cubie_type
        self.colors = cubie_colors
        self.correct_position = copy.copy(correct_position)
        self.position = copy.copy(correct_position)
