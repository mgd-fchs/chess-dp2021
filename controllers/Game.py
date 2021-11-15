# Composite class to handle game state and actions

# imports
import re
from enum import Enum

from controllers.Player import Player, ActiveState, InactiveState
from controllers.ChessBoard import ChessBoard
from controllers.FenParser import FenParser
from controllers.ChessPiece import *
from models.Chess import Chess, db

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
        # ensure correct move execution

        try:
            originSpot, destinationSpot, newFigure, castleType = self.parseMove(move)
        except TypeError:
            print("Error parsing move! Please check your input")
            return

        if castleType:
            moveMade = self.executeCastle(castleType)
        else: 
            moveMade = self.executeMove(originSpot, destinationSpot)
    
        if newFigure and (moveMade != -1):
            self.promotePawn(destinationSpot, newFigure)
        if moveMade != -1:
            self.togglePlayer()

    def executeMove(self, originSpot, destinationSpot):
        # execute a regular move

        piece = originSpot.getOccupant()

        if not piece:
            print("Cannot move piece from empty spot")
            return -1
        player = piece.getPlayer()

        if type(destinationSpot.getOccupant()) == King:
            takeKing = True
        else:
            print(str(destinationSpot.getOccupant()))
            takeKing = False
        
        # check validity of move
        valid = False
        for strategy in piece.getStrategy():
            valid = strategy.validateMove(self, originSpot, destinationSpot)
            if valid == True:
                print("This is a valid move!")
                break

        if valid == False:
            print("Please select a valid move!")
            return -1
        
        player.makeMove(originSpot, destinationSpot)
        
        if takeKing == True:
            self.setWinner(player.shortColor, "takeKing")

        # disable future casteling if rook or king have moved
        if type(piece) == King or type(piece) == Rook:
            self.toggleCastling(originSpot, piece)
        
        return 0

    def executeCastle(self, castleType):
        player = self.getActivePlayer()

        if castleType == "q":
            if player.getColor() == "white":
                originSpot = self.board[4][0]
                destinationSpot = self.board[2][0]
                rookOrigin = self.board[0][0]
                rookDestination = self.board[3][0]
                valid = self.checkValidMovement(originSpot.getOccupant(), originSpot, destinationSpot)
                if not valid:
                    return -1
                player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)
                
            if player.getColor() == "black":
                originSpot = self.board[4][7]
                destinationSpot = self.board[2][7]
                rookOrigin = self.board[0][7]
                rookDestination = self.board[3][7]
                valid = self.checkValidMovement(originSpot.getOccupant(), originSpot, destinationSpot)
                if not valid:
                    return -1
                player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)

        if castleType == "k":
            if player.getColor() == "white":
                originSpot = self.board[4][0]
                destinationSpot = self.board[6][0]
                rookOrigin = self.board[7][0]
                rookDestination = self.board[5][0]
                valid = self.checkValidMovement(originSpot.getOccupant(), originSpot, destinationSpot)
                if not valid:
                    return -1
                player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)

            if player.getColor() == "black":
                originSpot = self.board[4][7]
                destinationSpot = self.board[6][7]
                rookOrigin = self.board[7][7]
                rookDestination = self.board[5][7]
                valid = self.checkValidMovement(originSpot.getOccupant(), originSpot, destinationSpot)
                if not valid:
                    return -1
                player.executeCastle(originSpot, destinationSpot, rookOrigin, rookDestination)

        piece = originSpot.getOccupant()
        self.toggleCastling(originSpot, piece)
        return
    

    def promotePawn(self, destinationSpot, newFigure):

        validPromotion = False

        if destinationSpot.getOccupant().getColor() == "white":
            if destinationSpot.getPosition()[1] == 7:
                validPromotion = True
        if destinationSpot.getOccupant().getColor() == "black":
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

            newOccupant = newFigure(self.getActivePlayer())
            
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

        print("It's " + self.getActivePlayer().getColor() + "'s turn")

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
    
    def checkValidMovement(self, piece, originSpot, destinationSpot):
        # check validity of move
        if not piece:
            print("King is not in a position to castle!")
            return False

        valid = False
        for strategy in piece.getStrategy():
            valid = strategy.validateMove(self, originSpot, destinationSpot)
            if valid == True:
                print("This is a valid move!")
                break

        if valid == False:
            print("Please select a valid move!")
            return False
        return valid

    def setWinner(self, shortColor, condition):
        print("Setting winner")

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