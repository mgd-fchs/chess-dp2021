# imports
from abc import ABC, abstractmethod
import copy
from Strategy import MovementStrategy

# create the object at runtiume by copying the prototype instance
# common interface supports object cloning to decouple the code from the class of the method

class ChessPiecePrototype(ABC):
    def __init__(this):
        this.player = None
        this.symbol = None

    def move(this, originSpot, destinationSpot):
        print("Moved " + this.__class__.__name__ + " to: " + str(destinationSpot.getPosition()))
        if (MovementStrategy.validateMove()):
            originSpot.freeField()
            destinationSpot.occupyField(this)  # TODO: handle two figures on same spot! What if validation is wrong? -> go back to state

    @abstractmethod
    def clone(this):
        pass

# define differences for each type of figure
# symbol dependent on colour of player

class Pawn(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"

    def clone(this):
        return copy.deepcopy(this)

class Bishop(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"

    def clone(this):
        return copy.deepcopy(this)

class Knight(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"

    def clone(this):
        return copy.deepcopy(this)

class Rook(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"

    def clone(this):
        return copy.deepcopy(this)

class Queen(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"

    def clone(this):
        return copy.deepcopy(this)

class King(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"

    def clone(this):
        return copy.deepcopy(this)

# TODO: implement strategy for every call to move()