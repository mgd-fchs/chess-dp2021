# imports
from abc import ABC, abstractmethod
import copy
import controllers.Strategy as Strategy
from controllers.Strategy import MovementStrategy

# create the object at runtiume by copying the prototype instance
# common interface supports object cloning to decouple the code from the class of the method

class ChessPiecePrototype(ABC):
    def __init__(this):
        this.player = None
        this.symbol = None
        this.movementStrategy = MovementStrategy()
        this.color = None

    def setMovementStrategy(this, pieceStrategy):
        this.movementStrategy = pieceStrategy

    @abstractmethod
    def clone(this):
        pass

# define differences for each type of figure
# symbol dependent on colour of player

class Pawn(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.color = player.color
        this.symbol = "someImagePath"
        
        this.setMovementStrategy([Strategy.SingleForward, Strategy.SingleDiagonalForward])

    def clone(this):
        return copy.deepcopy(this)

class Bishop(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.color = player.color
        this.symbol = "someImagePath"

        this.setMovementStrategy([Strategy.MultipleDiagonal])

    def clone(this):
        return copy.deepcopy(this)

class Knight(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.color = player.color
        this.symbol = "someImagePath"

        this.setMovementStrategy([Strategy.TJump])

    def clone(this):
        return copy.deepcopy(this)

class Rook(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.symbol = "someImagePath"
        
        this.setMovementStrategy([Strategy.MultipleStraight])

    def clone(this):
        return copy.deepcopy(this)

class Queen(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.color = player.color
        this.symbol = "someImagePath"

        this.setMovementStrategy([Strategy.MultipleStraight, Strategy.MultipleDiagonal])

    def clone(this):
        return copy.deepcopy(this)

class King(ChessPiecePrototype):
    def __init__(this, player):
        super().__init__()
        this.player = player
        this.color = player.color
        this.symbol = "someImagePath"

        this.setMovementStrategy([Strategy.SingleForward, Strategy.SingleDiagonal])

    def clone(this):
        return copy.deepcopy(this)
