# Prototype class to generate chess pieces from
# Create the object at runtime by copying the prototype instance
# Common interface supports object cloning to decouple the code from the class of the method

# imports
from abc import ABC, abstractmethod
import copy
import controllers.Strategy as Strategy
from controllers.Strategy import MovementStrategy


class ChessPiecePrototype(ABC):
    def __init__(self):
        self._player = None
        self._symbol = None
        self._movementStrategy = MovementStrategy()
        self._color = None

    def setMovementStrategy(self, pieceStrategy):
        self._movementStrategy = pieceStrategy

    def getSymbol(self):
        if self._color == None:
            print("No color symbol found for piece " + str(self))
        if self._color == "white":
            return self._symbol.upper()
        else:
            return self._symbol
    
    def getColor(self):
        return self._color
    
    def getPlayer(self):
        return self._player

    def getStrategy(self):
        return self._movementStrategy

    @abstractmethod
    def clone(self):
        pass


# Define differences for each type of figure
# Symbol dependent on colour of player
class Pawn(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._color = self._player.getColor()
        self._symbol = "p"
        
        try:
            self.setMovementStrategy([Strategy.SingleForward, Strategy.SingleDiagonalForward, Strategy.DoubleForward])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")

    def clone(self):
        return copy.deepcopy(self)


class Bishop(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._color = player.getColor()
        self._symbol = "b"

        try:
            self.setMovementStrategy([Strategy.MultipleDiagonal])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")
    
    def clone(self):
        return copy.deepcopy(self)


class Knight(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._color = player.getColor()
        self._symbol = "n"

        try:
            self.setMovementStrategy([Strategy.TJump])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")
    
    def clone(self):
        return copy.deepcopy(self)


class Rook(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._color = player.getColor()
        self._symbol = "r"
        
        try:
            self.setMovementStrategy([Strategy.MultipleStraight])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")        

    def clone(self):
        return copy.deepcopy(self)


class Queen(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._color = player.getColor()
        self._symbol = "q"
        
        try:
            self.setMovementStrategy([Strategy.MultipleStraight, Strategy.MultipleDiagonal])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")

    def clone(self):
        return copy.deepcopy(self)


class King(ChessPiecePrototype):
    def __init__(self, player):
        super().__init__()
        self._player = player
        self._color = player.getColor()
        self._symbol = "k"

        try:
            self.setMovementStrategy([Strategy.SingleForward, Strategy.SingleDiagonal, Strategy.CastleKingside, Strategy.CastleQueenside])
        except AttributeError:
            print("Movement strategy not found for " + str(self) + "!")

    def clone(self):
        return copy.deepcopy(self)
