# imports
from abc import ABC, abstractmethod
import copy
# import BoardSpot

# create the object at runtiume by copying the prototype instance
# common interface supports object cloning to decouple the code from the class of the method
# https://stackabuse.com/the-prototype-design-pattern-in-python/

class ChessPiecePrototype(ABC):
    def __init__(this):
        this.player = None
        this.symbol = None

    def move(this, boardSpot):
        print("Moved " + this.__class__.__name__ + " to: " + boardSpot.__class__.__name__)
        pass

    @abstractmethod
    def clone(this):
        pass

# define differences for each type of figure

class Pawn(ChessPiecePrototype):
    def __init__(this, player, symbol):
        super().__init__()

    def clone(this):
        return copy.deepcopy(this)

class Bishop(ChessPiecePrototype):
    def __init__(this, player, symbol):
        super().__init__()

    def clone(this):
        return copy.deepcopy(this)

class Knight(ChessPiecePrototype):
    def __init__(this, player, symbol):
        super().__init__()

    def clone(this):
        return copy.deepcopy(this)

class Rook(ChessPiecePrototype):
    def __init__(this, player, symbol):
        super().__init__()

    def clone(this):
        return copy.deepcopy(this)

class Queen(ChessPiecePrototype):
    def __init__(this, player, symbol):
        super().__init__()

    def clone(this):
        return copy.deepcopy(this)

class King(ChessPiecePrototype):
    def __init__(this, player, symbol):
        super().__init__()

    def clone(this):
        return copy.deepcopy(this)

# TODO: implement strategy for ever call to move()