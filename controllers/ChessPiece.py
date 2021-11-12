# imports
from abc import ABC, abstractmethod
import copy
import controllers.Strategy as Strategy
from controllers.Strategy import MovementStrategy

# create the object at runtime by copying the prototype instance
# common interface supports object cloning to decouple the code from the class of the method

class ChessPiecePrototype(ABC):
    def __init__(self):
        self.player = None
        self.symbol = None
        self.movementStrategy = MovementStrategy()
        self.color = None

    def setMovementStrategy(self, pieceStrategy):
        self.movementStrategy = pieceStrategy

    def getSymbol(self):
        if self.color == None:
            print("No color symbol found for piece " + str(self))
        if self.color == "white":
            return self.symbol.upper()
        else:
            return self.symbol

    @abstractmethod
    def clone(self):
        pass

# define differences for each type of figure
# symbol dependent on colour of player

class Pawn(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.color = player.color
        self.symbol = "p"
        
        try:
            self.setMovementStrategy([Strategy.SingleForward, Strategy.SingleDiagonalForward, Strategy.DoubleForward])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")

    def clone(self):
        return copy.deepcopy(self)

class Bishop(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.color = player.color
        self.symbol = "b"

        try:
            self.setMovementStrategy([Strategy.MultipleDiagonal])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")
    
    def clone(self):
        return copy.deepcopy(self)

class Knight(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.color = player.color
        self.symbol = "n"

        try:
            self.setMovementStrategy([Strategy.TJump])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")
    
    def clone(self):
        return copy.deepcopy(self)

class Rook(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.color = player.color
        self.symbol = "r"
        
        try:
            self.setMovementStrategy([Strategy.MultipleStraight])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")        

    def clone(self):
        return copy.deepcopy(self)

class Queen(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.color = player.color
        self.symbol = "q"
        
        try:
            self.setMovementStrategy([Strategy.MultipleStraight, Strategy.MultipleDiagonal])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")

    def clone(self):
        return copy.deepcopy(self)

class King(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.color = player.color
        self.symbol = "k"

        try:
            self.setMovementStrategy([Strategy.SingleForward, Strategy.SingleDiagonal, Strategy.CastleKingside, Strategy.CastleQueenside])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")

    def clone(self):
        return copy.deepcopy(self)
