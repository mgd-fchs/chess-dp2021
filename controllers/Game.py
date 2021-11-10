# Composite class
from controllers.Player import Player, ActiveState, InactiveState
from controllers.ChessBoard import ChessBoard
from controllers.FenParser import FenParser
from models.Chess import Chess, db

from enum import Enum


class State(Enum):
    INIT = 1
    PLAY = 2
    END = 3

class Game:

    def __init__(this, fen):
        # instantiate players
        this.whitePlayer = Player("white")
        this.blackPlayer = Player("black")

        this.activePlayer = None
        this.gameState = State.INIT
        # example fen string: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        this.gameString = fen
        this.board = None

        # instantiate board
        this.gameState = State.PLAY
        this.fullmove_number = 1
        this.parser = FenParser(this)
        this.parseFenString(this.gameString)

    def move(self, move):
        # parse move
        originSpot, destinationSpot = self.parseMove(move)
        self.executeMove(originSpot, destinationSpot)

    def executeMove(this, originSpot, destinationSpot):
        piece = originSpot.getOccupant()

        if not piece:
            print("Cannot move piece from empty spot")
            return

        player = piece.player

        valid = False
        for strategy in piece.movementStrategy:
            valid = strategy.validateMove(this, originSpot, destinationSpot)
            if valid == True:
                print("This is a valid move!")
                break

        if valid == False:
            print("Please select a valid move!")
            return

        player.makeMove(originSpot, destinationSpot)
        this.togglePlayer()

    def end(this):
        # to be called when a player wins or gives up
        # ends the application
        this.gameState = State.END
        pass

    def undo(this):
        # TODO
        pass

    def redo(this):
        # TODO
        pass

    def reset(this):
        # TODO
        pass

    def replay(this):
        # TODO
        pass

    def getFenString(this):
        return this.parser.getFenString()
    
    def parseFenString(this, fenStr):
        return this.parser.parseFenString(fenStr)

    def parseMove(this, move):
        return this.parser.parseMove(move)

    def togglePlayer(this):
        if this.activePlayer == this.whitePlayer:
            this.activePlayer = this.blackPlayer
            this.blackPlayer.setState(ActiveState())
            this.whitePlayer.setState(InactiveState())
        else:
            this.activePlayer = this.whitePlayer
            this.blackPlayer.setState(ActiveState())
            this.whitePlayer.setState(InactiveState())
            this.fullmove_number += 1
        print("now its " + this.activePlayer.color + "'s turn")

    def getActivePlayer(self):
        return self.activePlayer
