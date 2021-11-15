# Player class provides state-dependent behaviour

# imports
from abc import ABC, abstractmethod

class Player():
    _instances = []

    def __init__(self, color):

        self._color = color
        self.queenCastle = False
        self.kingCastle = False

        if color == "white":
            self.shortColor = "w"
            self.setState(ActiveState())
        elif color == "black":
            self.shortColor = "b"
            self.setState(InactiveState())

        self._instances.append(self)

    def setState(self, state):
        self._state = state
        self._state.player = self

    def makeMove(self, originField, destinationField):
        self._state.makeMove(originField, destinationField)
    
    def executeCastle(self, originField, destinationField, rookOrigin, rookDestination):
        self._state.executeCastle(originField, destinationField, rookOrigin, rookDestination)

    def getState(self):
        return self._state

    def getColor(self):
        return self._color

    def setKingCastle(self):
        self.kingCastle = True

    def setQueenCastle(self):
        self.queenCastle = True
    
    def removeKingCastle(self):
        self.kingCastle = True

    def removeQueenCastle(self):
        self.queenCastle = True



class State(ABC):
    @property
    def context(self):
        return self._player

    @context.setter
    def player(self, player):
        self._player = player

    @abstractmethod
    def makeMove(self, originField, destinationField):
        pass

    @abstractmethod
    def giveUp(self):
        pass


class ActiveState(State):
    def makeMove(self, originField, destinationField):
        movingPiece = originField.getOccupant()

        print("Moving piece " + str(originField.getOccupant()) + " to " + str(destinationField.getPosition()))
        originField.freeField()
        destinationField.freeField()
        destinationField.occupyField(movingPiece)

        self.player.setState(InactiveState())

        # Activate other player
        playerInstance = Player._instances.index(self.player)
        if playerInstance == 1:
            Player._instances[0].setState(ActiveState())
        elif playerInstance == 0:
            Player._instances[1].setState(ActiveState())

        return 0

    def executeCastle(self, originField, destinationField, rookOrigin, rookDestination):
        king = originField.getOccupant()
        rook = rookOrigin.getOccupant()

        originField.freeField()
        destinationField.occupyField(king)

        rookOrigin.freeField()
        rookDestination.occupyField(rook)        

        # Activate other player
        playerInstance = Player._instances.index(self.player)
        if playerInstance == 1:
            Player._instances[0].setState(ActiveState())
        elif playerInstance == 0:
            Player._instances[1].setState(ActiveState())
        return 0

    def giveUp(self):
        print("Giving up")
        # set winning state to other player


class InactiveState(State):
    def makeMove(self, originField, destinationField):
        print("Cannot make move. It's not your turn")
        return -1

    def executeCastle(self, originField, destinationField, rookOrigin, rookDestination):
        print("Cannot make move. It's not your turn")
        return -1

    def giveUp(self):
        print("Giving up")
        # set winning state to other player
