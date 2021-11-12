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

    def __init__(self, fen):
        # instantiate players
        self.whitePlayer = Player("white")
        self.blackPlayer = Player("black")
        self.winner = None

        self.activePlayer = None
        self.gameState = State.INIT
        self.gameString = fen
        self.board = None

        # instantiate board
        self.gameState = State.PLAY
        self.fullmove_number = 1
        self.halfmove_clock = 0
        self.parser = FenParser(self)
        self.parseFenString(self.gameString)

    def move(self, move):
        # parse move
        try:
            originSpot, destinationSpot, newFigure = self.parseMove(move)
        except TypeError:
            print("Error parsing move! Please check your input")
            return

        moveMade = self.executeMove(originSpot, destinationSpot)
        
        if newFigure and (moveMade != -1):
            self.promotePawn(destinationSpot, newFigure)

        # TODO: Check if this can be done via state pattern only!
        self.togglePlayer()

    def executeMove(self, originSpot, destinationSpot):
        piece = originSpot.getOccupant()

        if not piece:
            print("Cannot move piece from empty spot")
            return -1
        player = piece.player

        if type(destinationSpot.getOccupant()) == King:
            takeKing = True
        else:
            print(str(destinationSpot.getOccupant()))
            takeKing = False
        
        # check validity of move
        valid = False
        for strategy in piece.movementStrategy:
            valid, castleMove = strategy.validateMove(self, originSpot, destinationSpot)
            if valid == True:
                print("This is a valid move!")
                break

        if valid == False:
            print("Please select a valid move!")
            return -1
        
        # handle casteling
        if castleMove:
            if castleMove == "q":
                if player.color == "white":
                    rookOrigin = self.board[0][0]
                    rookDestination = self.board[3][0]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
                if player.color == "black":
                    rookOrigin = self.board[0][7]
                    rookDestination = self.board[3][7]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)

            if castleMove == "k":
                if player.color == "white":
                    rookOrigin = self.board[7][0]
                    rookDestination = self.board[5][0]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
                if player.color == "black":
                    rookOrigin = self.board[7][7]
                    rookDestination = self.board[5][7]
                    player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
        else:
            player.makeMove(originSpot, destinationSpot)
            if takeKing == True:
                self.setWinner(player.shortColor, "takeKing")

        # disable future casteling if rook or king have moved
        if type(piece) == King or type(piece) == Rook:
            self.toggleCastling(originSpot, piece)


    def promotePawn(self, destinationSpot, newFigure):
        validPromotion = False

        if destinationSpot.getOccupant().color == "white":
            if destinationSpot.getPosition()[1] == 7:
                validPromotion = True
        if destinationSpot.getOccupant().color == "black":
            if destinationSpot.getPosition()[1] == 0:
                validPromotion = True
       
        if validPromotion:
            print("Promoting pawn...")

            if type(newFigure) == Pawn:
                print("Cannot promote to pawn!")
                return
            
            if type(newFigure) == King:
                print("Cannot promote to king!")
                return

            newOccupant = newFigure(self.activePlayer)
            
            print("...to " + str(type(newOccupant)))
            destinationSpot.occupyField(newOccupant)

    def end(self):
        # to be called when a player wins or gives up
        # ends the application
        self.gameState = State.END
        pass

    def getFenString(self):
        return self.parser.getFenString()
    
    def parseFenString(self, fenStr):
        return self.parser.parseFenString(fenStr)

    def parseMove(self, move):
        return self.parser.parseMove(move)

    def togglePlayer(self):
        if self.activePlayer == self.whitePlayer:
            self.activePlayer = self.blackPlayer
            self.blackPlayer.setState(ActiveState())
            self.whitePlayer.setState(InactiveState())
        else:
            self.activePlayer = self.whitePlayer
            self.blackPlayer.setState(ActiveState())
            self.whitePlayer.setState(InactiveState())
            self.fullmove_number += 1

        print("It's " + self.activePlayer.color + "'s turn")

    def getActivePlayer(self):
        return self.activePlayer

    def toggleCastling(self, piece, originSpot):
        # once either the king or rook have moved, castling is no onger allowed
        if type(piece) == King:
            self.activePlayer.removeKingCastle()
            self.activePlayer.removeQueenCastle()
        
        if type(piece) == Rook:
            if originSpot.getPosition()[0] == 7:
                if self.activePlayer == self.whitePlayer:
                    self.activePlayer.removeKingCastle()
                elif self.activePlayer == self.blackPlayer:
                    self.activePlayer.removeQueenCastle()

            elif originSpot.getPosition()[0] == 0:
                if self.activePlayer == self.whitePlayer:
                    self.activePlayer.removeQueenCastle()
                elif self.activePlayer == self.blackPlayer:
                    self.activePlayer.removeKingCastle()
           
    def setWinner(self, shortColor, condition):
        print("Setting winner")
        # TODO: Replace condition strings (?)
        if shortColor == "w":
            self.winner = "white"
        else: self.winner = "black"

        if condition == "fiftyMoves":
            print("Game ended in draw!")
            self.winner = "Neither player"
            self.end()

        elif condition == "giveUp":
            print(str(self.winner) + " is the winner!")
            self.end()

        elif condition == "takeKing":
            print(str(self.winner) + " is the winner!")
            self.end()
        else: print("Unknown winning condition")