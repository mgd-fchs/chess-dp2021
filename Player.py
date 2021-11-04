# imports
from abc import ABC, abstractmethod
from ChessBoard import BoardSpot
import ChessPiece

class Player ():
    _instances = []
    def __init__(this, color):
        if len(this._instances) > 2:
            raise Warning("More than 2 player instances created but only 2 can play!")

        _playerColor = color

        if color == "white":
            this.setState(ActiveState())
        elif color == "black":
            this.setState(InactiveState())
        else: 
            raise ValueError("Player color must be black or white, but was " + str(color))
        
        this._instances.append(this)
    
    def setState(this, state):
        this._state = state
        this._state.player = this

    def makeMove(this, originField, destinationField):
        this._state.makeMove(originField, destinationField) 
    

class State(ABC):
    @property
    def context(this):
        return this._player

    @context.setter
    def player(this, player):
        this._player = player

    @abstractmethod
    def makeMove(this, originField, destinationField):
        pass

    @abstractmethod
    def giveUp(this):
        pass

class ActiveState(State):
    def makeMove(this, originField, destinationField):
        print("Moving pieces")
        # Inactivate current player after making a move
        this.player.setState(InactiveState())

        # TODO: Move piece

        # Activate other player
        playerInstance = Player._instances.index(this.player)
        if playerInstance == 1:
            Player._instances[0].setState(ActiveState())
        elif playerInstance == 0:
            Player._instances[1].setState(ActiveState())

    def giveUp(this):
        print("Giving up")
        # set winning state to other player

class InactiveState(State):
    def makeMove(this, originField, destinationField):
        print("Cannot make move. It's not your turn")

    def giveUp(this):
        print("Giving up")
        # set winning state to other player