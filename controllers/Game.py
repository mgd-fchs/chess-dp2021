# Composite class
import re

from controllers.Player import Player, ActiveState, InactiveState
from controllers.ChessBoard import ChessBoard
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
        this.parseFenString(this.gameString)

        # TODO: Instantiate other components: e.g. History

    def parseFenString(self, gameString):
        params = gameString.split()
        if len(params) != 6:
            return -1

        lines = params[0].split("/")
        if len(lines) != 8:
            return -1
        self.board = ChessBoard().setPieces(lines, self.whitePlayer, self.blackPlayer)

        active_player = params[1]
        if re.match("^[w]$", active_player):
            self.whitePlayer.setState(ActiveState())
            self.blackPlayer.setState(InactiveState())
            self.activePlayer = self.whitePlayer
        elif re.match("^[b]$", active_player):
            self.blackPlayer.setState(ActiveState())
            self.whitePlayer.setState(InactiveState())
            self.activePlayer = self.blackPlayer
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

        self.fullmove_number = int(fullmove_number)

    def getFenString(self):
        lines = ""
        lineNumber = 0
        rowNumber = 0
        jumpover = 0

        # transpose board matrix and traverse it in reversed order
        for line in reversed(list(map(list, zip(*self.board)))):
            for pos in line:
                if pos.getOccupant() != None:
                    if jumpover != 0:
                        lines += str(jumpover)
                        jumpover = 0
                    lines += pos.getOccupant().getSymbol()
                else:
                    jumpover += 1
                rowNumber += 1

            if jumpover != 0:
                lines += str(jumpover)
                jumpover = 0
            lineNumber += 1
            rowNumber = 0
            if lineNumber != len(self.board):
                lines += "/"

        # Add Players turn
        lines += " "
        lines += self.activePlayer.shortColor

        # TODO
        # Add possible casteling options
        lines += " KQkq"

        # Add enpassant options
        lines += " -"

        # Add halfmove clock
        lines += " 0"

        # Add fullmove number
        lines += " "
        lines += str(self.fullmove_number)

        return lines

    def move(self, move):
        # parse move
        if move == "0-0" or move == "0-0-0":
            # TODO casteling
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

        if not re.match("^[a-h]$", move_from_row) or \
                not re.match("^[1-8]$", move_from_line) or \
                not re.match("^[a-h]$", move_to_row) or \
                not re.match("^[1-8]$", move_to_line) or \
                not re.match("^(?i)r|n|b|q|k|p$", figure):
            # TODO Error handling
            print("error")
            return

        # check right player
        if re.match("^r|n|b|q|k|p$", figure) and self.activePlayer.shortColor != "b":
            # TODO Error handling
            print("not right player " + str(self.activePlayer.shortColor) + " " + str(figure))
            return

        # transfer row a-h to numbers
        move_to_row = ord(move_to_row) - 96
        move_from_row = ord(move_from_row) - 96

        # check if the right figure is selected
        originSpot = self.board[int(move_from_row) - 1][int(move_from_line) - 1]
        if originSpot.getOccupant() != None:
            if originSpot.getOccupant().getSymbol() != figure:
                print("wrong figure selected " + originSpot.getOccupant().getSymbol())
                return
        destinationSpot = self.board[int(move_to_row) - 1][int(move_to_line) - 1]

        # execute and check if the move can be done
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
        currentFen = this.getFenString()
        # store in gameID table:
        # moveID, currentFen
        # TODO: Replace print statements with proper messages/warnings

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
        print("now its " + this.activePlayer.shortColor + " turn")

    def getActivePlayer(self):
        return self.activePlayer
