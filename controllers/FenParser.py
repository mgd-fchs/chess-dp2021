from controllers.ChessBoard import ChessBoard
from controllers.Player import Player, ActiveState, InactiveState
from controllers.ChessPiece import *
import re

class FenParser():

    def __init__(self, game):
        self.game = game

    def parseFenString(self, gameString):
        params = gameString.split()
        if len(params) != 6:
            return -1

        lines = params[0].split("/")
        if len(lines) != 8:
            return -1
        self.game.board = ChessBoard().setPieces(lines, self.game.whitePlayer, self.game.blackPlayer)

        active_player = params[1]
        if re.match("^[w]$", active_player):
            self.game.whitePlayer.setState(ActiveState())
            self.game.blackPlayer.setState(InactiveState())
            self.game.activePlayer = self.game.whitePlayer
        elif re.match("^[b]$", active_player):
            self.game.blackPlayer.setState(ActiveState())
            self.game.whitePlayer.setState(InactiveState())
            self.game.activePlayer = self.game.blackPlayer
        else:
            print("wrong player param")
            return -1

        casteling = params[2]
        if not re.match("(^K?Q?k?q?$)|(^-$)", casteling):
            return -1
        else:
            self.setCastelingCondition(casteling)

        en_passant = params[3]
        if not re.match("(^[a-h](3|6)$)|(^-$)", en_passant):
            return -1

        if en_passant != "-":
            print("passant present")
            xPos, yPos = self.getPositionFromFen(en_passant)
            if xPos and yPos:
                self.game.board[xPos][yPos].setPassant()

        halfmove_clock = params[4]
        if not re.match("^(0|[1-9][0-9]*)$", halfmove_clock):
            return -1

        self.game.halfmove_clock = int(halfmove_clock)
        if int(halfmove_clock) >= 50:
            self.game.setWinner(active_player, "fivtyMoves")

        fullmove_number = params[5]
        if not re.match("^(0|[1-9][0-9]*)$", fullmove_number):
            return -1

        self.game.fullmove_number = int(fullmove_number)
        

    def parseMove(self, move):

        move = move.split()
        switchFigure = None
        castelingType = None

        if len(move) == 1:
            # casteling

            if move[0] == "0-0":
                print("Kingside casteling!")
                castelingType = "k"
                return None, None, None, castelingType

            elif move[0] == "0-0-0":
                print("Queenside casteling!")
                castelingType = "q"
                return None, None, None, castelingType

        elif len(move) < 2:
            print("Please enter a valid move! Parser takes input of length 2 or 3 but was: " + str(len(move)))
            return
        elif len(move) > 3:
            print("Please enter a valid move! Parser takes input of length 2 or 3 but was: " + str(len(move)))
            return

        # normal move
        if len(move) == 2:
            move_from = move[0]
            move_to = move[1]

        # a promotion
        if len(move) == 3:
            move_from = move[0]
            move_to = move[1]
            switch_to = move[2]
            switchFigure = self.getFigureFromFen(switch_to)

        if move_from[0] != move_to[0]:
            print("Wrong input, must move the same figure. Input was:" + str(move_from) + " " + str(move_to) + ".")
            return

        figure = move_from[0]
        move_from_line = move_from[2]
        move_from_row = move_from[1]

        move_to_line = move_to[2]
        move_to_row = move_to[1]

        if not re.match("^[a-h]$", move_from_row):
            print("Incorrect input: Cannot move piece from row " + str(move_from_row))
            return
        elif not re.match("^[1-8]$", move_from_line):
            print("Incorrect input: Cannot move piece from line " + str(move_from_line))
            return
        elif not re.match("^[a-h]$", move_to_row):
            print("Incorrect input: Cannot move piece to row " + str(move_to_row))
            return
        elif not re.match("^[1-8]$", move_to_line):
            print("Incorrect input: Cannot move piece to row " + str(move_to_line))             
        elif not re.match("^(?i)r|n|b|q|k|p$", figure):
            print("Incorrect input: Cannot move piece  " + str(figure)) 
            return

        # check right player
        if re.match("^r|n|b|q|k|p$", figure) and self.game.activePlayer.shortColor != "b":
            # TODO Error handling
            print("not right player " + str(self.game.activePlayer.shortColor) + " " + str(figure))
            return

        # transfer row a-h to numbers
        move_to_row = ord(move_to_row) - 96
        move_from_row = ord(move_from_row) - 96

        # check if the right figure is selected
        originSpot = self.game.board[int(move_from_row)-1][int(move_from_line)-1]
        if originSpot.getOccupant() != None:
            if originSpot.getOccupant().getSymbol() != figure:
                print("Wrong figure selected: " + originSpot.getOccupant().getSymbol())
                return
        destinationSpot = self.game.board[int(move_to_row)-1][int(move_to_line)-1]
        return (originSpot, destinationSpot, switchFigure, castelingType)

    def getFenString(self):
        lines = ""
        lineNumber = 0
        rowNumber = 0
        jumpover = 0
        enPassantPos = None

        # transpose board matrix and traverse it in reversed order
        for line in reversed(list(map(list, zip(*self.game.board)))):
            for pos in line:
                if pos.getOccupant() != None:
                    if jumpover != 0:
                        lines += str(jumpover)
                        jumpover = 0
                    lines += pos.getOccupant().getSymbol()
                else:
                    if pos.getPassant():
                        enPassantPos = pos
                    jumpover += 1
                rowNumber += 1

            if jumpover != 0:
                lines += str(jumpover)
                jumpover = 0
            lineNumber += 1
            rowNumber = 0
            if lineNumber != len(self.game.board):
                lines += "/"

        # Add Players turn
        lines += " "
        lines += self.game.activePlayer.shortColor

        # TODO
        # Add castling option
        castleStr = " "
        if self.game.whitePlayer.kingCastle == True:
            castleStr += "K"
        if self.game.whitePlayer.queenCastle == True:
            castleStr += "Q"
        if self.game.blackPlayer.kingCastle == True:
            castleStr += "k"
        if self.game.blackPlayer.queenCastle == True:
            castleStr += "q"
        if castleStr == " ":
            castleStr += "-"

        lines += castleStr

        # Add enpassant option
        if enPassantPos != None:
            lines += self.getFenFromPosition(enPassantPos)
            enPassantPos.removePassant()
        else: lines += " -"

        # Add halfmove clock
        lines += " "
        lines += str(self.game.halfmove_clock)

        # Add fullmove number
        lines += " "
        lines += str(self.game.fullmove_number)

        return lines
    
    def getFenFromPosition(self, spot):
        # get algebraic representation of board position
        # e.g. board position (0,2) returns 'a3'

        alph = "abcdefgh"
        xPos = spot.getPosition()[0]
        yPos = spot.getPosition()[1]

        xString = alph[xPos]
        yString = str(yPos + 1)

        return " " + xString + yString

    def getPositionFromFen(self, fenStr):
        alph = "abcdefgh"
        xPos = None
        yPos = None
        if fenStr == "-":
            return xPos, yPos

        xPos = alph.index(fenStr[0])
        yPos = int(fenStr[1])-1
        
        return xPos, yPos

    def setCastelingCondition(self, castleString):
        # set castling parameters in player class
        if "K" in castleString:
            self.game.whitePlayer.setKingCastle()
        if "Q" in castleString:
            self.game.whitePlayer.setQueenCastle()
        if "k" in castleString:
            self.game.blackPlayer.setKingCastle()
        if "q" in castleString:
            self.game.blackPlayer.setQueenCastle()

    def getFigureFromFen(self, figureStr):
        figureDict = {"p" : Pawn,
                    "r" : Rook,
                    "b" : Bishop,
                    "n" : Knight,
                    "q" : Queen,
                    "k" : King}

        if figureStr.lower() not in figureDict.keys():
            print("No such figure exists: " + str(figureStr))
            return
        else:
            figureType = figureDict[figureStr.lower()]

        return figureType
