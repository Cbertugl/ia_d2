from enum import IntEnum

# Sudoku tiles possible values, our CSP domain
class Domain(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @staticmethod
    def getAsArray():
        return list(map(int, Domain))

NO_VALUE = 0

GRID_SIZE = 9

FAILURE = -1
