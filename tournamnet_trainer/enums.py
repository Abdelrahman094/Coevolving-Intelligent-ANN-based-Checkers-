from enum import Enum

class Position(Enum):
    Empty = '0'
    Black = 'b'
    BlackKing = 'B'
    White = 'w'
    WhiteKing = 'W'
    Undefined = '-'

class Player(Enum):
    Black = 'B'
    White = 'W'