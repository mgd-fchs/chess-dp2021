# Composite class
import re

from controllers.Player import Player, ActiveState, InactiveState
from controllers.ChessBoard import ChessBoard
from controllers.FenParser import FenParser
from controllers.ChessPiece import *
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
        this.gameString = fen
        this.board = None

        # instantiate board
        this.gameState = State.PLAY
        this.fullmove_number = 1
        this.halfmove_clock = 0
        this.parser = FenParser(this)
        this.parseFenString(this.gameString)

    def move(self, move):
        # parse move
        try:
            originSpot, destinationSpot = self.parseMove(move)
        except TypeError:
            print("Error parsing move! Please check your input")
            return
        
        self.executeMove(originSpot, destinationSpot)

    def executeMove(this, originSpot, destinationSpot):
        piece = originSpot.getOccupant()

        if not piece:
            print("Cannot move piece from empty spot")
            return

        player = piece.player

        # check validity of move
        valid = False
        for strategy in piece.movementStrategy:
            valid, castleMove = strategy.validateMove(this, originSpot, destinationSpot)
            if valid == True:
                print("This is a valid move!")
                break

        if valid == False:
            print("Please select a valid move!")
            return
        
        # handle casteling
        if castleMove:
            if castleMove == "q":
                if player.color == "white":
                    rookOrigin = this.board[0][0]
                    rookDestination = this.board[3][0]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
                if player.color == "black":
                    rookOrigin = this.board[0][7]
                    rookDestination = this.board[3][7]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)

            if castleMove == "k":
                if player.color == "white":
                    rookOrigin = this.board[7][0]
                    rookDestination = this.board[5][0]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
                if player.color == "black":
                    rookOrigin = this.board[7][7]
                    rookDestination = this.board[5][7]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
        else:
            player.makeMove(originSpot, destinationSpot)

        # disable future casteling if rook or king have moved
        if type(piece) == King or type(piece) == Rook:
            this.toggleCastling(originSpot, piece)

        # TODO: Check if this can be done via state pattern only!
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
        print("It's " + this.activePlayer.color + "'s turn")

    def getActivePlayer(self):
        return self.activePlayer

    def toggleCastling(self, piece, originSpot):
        # once either the king or rook have moved, castling is no onger allowed
        if type(piece) == King:
            this.activePlayer.removeKingCastle()
            this.activePlayer.removeQueenCastle()
        
        if type(piece) == Rook:
            if originSpot.getPosition()[0] == 7:
                if this.activePlayer == this.whitePlayer:
                    this.activePlayer.removeKingCastle()
                elif this.activePlayer == this.blackPlayer:
                    this.activePlayer.removeQueenCastle()

            elif originSpot.getPosition()[0] == 0:
                if this.activePlayer == this.whitePlayer:
                    this.activePlayer.removeQueenCastle()
                elif this.activePlayer == this.blackPlayer:
                    this.activePlayer.removeKingCastle()
           
    def setWinner(self, shortColor, fivtyMoves = True):

        if fivtyMoves == True:
            print("Game ended in draw!")
            # self.end()
        else: print(str(shortColor) + " is the winner!")
            # display winner
            # self.end()