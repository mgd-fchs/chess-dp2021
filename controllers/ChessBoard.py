# Chess board class to set up initial state of the board and generate playable positions
# Composite class

# imports
import re
from controllers import ChessPiece

class ChessBoard:
    _positions = []

    def __init__(this):
        pass

    def setPieces(this, lines, whitePlayer, blackPlayer):
        # Lines are in form of: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
        # Uppercase is a white figure, lowercase a black
        # Numbers are the left free spots

        # initialize board by creating playable fields
        this._positions = []
        for i in range(0, 8):
            this._positions.append([])
            for j in range(0, 8):
                this._positions[i].append(BoardSpot(i, j))

        # set the pieces to their positions
        line_number = 0
        row_number = 0
        for line in lines:
            line = line[::-1]
            for char in line:
                if re.match("^[1-8]$", char):
                    row_number += int(char) - 1
                elif re.match("^(?i)r|n|b|q|k|p$", char):
                    color = blackPlayer
                    if re.match("^R|N|B|Q|K|P$", char):
                        color = whitePlayer
                    if re.match("^(?i)r$", char):
                        chess_piece = ChessPiece.Rook(color)
                    elif re.match("^(?i)n$", char):
                        chess_piece = ChessPiece.Knight(color)
                    elif re.match("^(?i)b$", char):
                        chess_piece = ChessPiece.Bishop(color)
                    elif re.match("^(?i)q$", char):
                        chess_piece = ChessPiece.Queen(color)
                    elif re.match("^(?i)k$", char):
                        chess_piece = ChessPiece.King(color)
                    elif re.match("^(?i)p$", char):
                        chess_piece = ChessPiece.Pawn(color)
                    else:
                        return -1
                    this._positions[7-row_number][7-line_number].occupyField(chess_piece)

                else:
                    return -1
                row_number += 1
            row_number = 0
            line_number += 1
        return this._positions


class BoardSpot():
    def __init__(this, xPosition, yPosition):
        this._xPos = xPosition
        this._yPos = yPosition
        this._occupant = None
        this._passant = False

    def occupyField(this, chessPiece):
        this._occupant = chessPiece
        # notify logger here or in main class?

    def getOccupant(this):
        return this._occupant

    def freeField(this):
        this._occupant = None

    def getPosition(this):
        # getter function for coordinates        
        position = tuple((this._xPos, this._yPos))
        return position
    
    def setPassant(this):
        this._passant = True

    def getPassant(this):
        return this._passant

    def removePassant(this):
        this._passant = None