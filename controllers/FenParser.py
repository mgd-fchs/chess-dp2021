from controllers.ChessBoard import ChessBoard
from controllers.Player import Player, ActiveState, InactiveState
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

        en_passant = params[3]
        if not re.match("(^[a-h](3|6)$)|(^-$)", en_passant):
            return -1

        halfmove_clock = params[4]
        if not re.match("^(0|[1-9][0-9]*)$", halfmove_clock):
            return -1

        fullmove_number = params[5]
        if not re.match("^(0|[1-9][0-9]*)$", fullmove_number):
            return -1

        self.game.fullmove_number = int(fullmove_number)
        

    def parseMove(self, move):

        if move == "0-0" or move == "0-0-0":
        #TODO casteling
            print("TODO casteling")
            return

        move = move.split()
        # normal move
        if len(move) == 2:
            move_from = move[0]
            move_to = move[1]

        # a pawn
        if len(move) == 3:
            move_from = move[0]
            move_to = move[1]
            switch_to = move[2]

        if len(move_from) != 3 or len(move_to) != 3 or move_from[0] != move_to[0]:
            print("wrong input" + str(len(move_from)))
            return

        figure = move_from[0]
        move_from_line = move_from[2]
        move_from_row = move_from[1]

        move_to_line = move_to[2]
        move_to_row = move_to[1]

        if not re.match("^[a-h]$", move_from_row) or\
                not re.match("^[1-8]$", move_from_line) or \
                not re.match("^[a-h]$", move_to_row) or \
                not re.match("^[1-8]$", move_to_line) or \
                not re.match("^(?i)r|n|b|q|k|p$", figure):
            # TODO Error handling
            print("error")
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
                print("wrong figure selected " + originSpot.getOccupant().getSymbol())
                return
        destinationSpot = self.game.board[int(move_to_row)-1][int(move_to_line)-1]
        return (originSpot, destinationSpot)

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
        # Add possible casteling options
        lines += " KQkq"

        # Add enpassant option
        if enPassantPos != None:
            lines += self.getPositionFen(enPassantPos)
        else: lines += " -"

        # Add halfmove clock
        lines += " 0"

        # Add fullmove number
        lines += " "
        lines += str(self.game.fullmove_number)

        return lines
    
    def getPositionFen(self, spot):
        # get algebraic representation of board position
        # e.g. board position (0,2) returns 'a3'

        alph = "abcdefgh"
        xPos = spot.getPosition()[0]
        yPos = spot.getPosition()[1]

        xString = alph[xPos]
        yString = alph[yPos]

        return " " + xString + yString

