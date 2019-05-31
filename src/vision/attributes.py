from enum import IntEnum

class Shapes(IntEnum):
    DIAMOND, SQUIGGLE, OVAL = 0, 1, 2

class Colors(IntEnum):
    GREEN, RED, PURPLE = 0, 1, 2

class Fills(IntEnum):
    FULL, STRIPE, HOLLOW = 0, 1, 2

class Counts(IntEnum):
    ONE, TWO, THREE = 0, 1, 2