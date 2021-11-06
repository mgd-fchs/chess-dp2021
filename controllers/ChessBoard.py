# imports
import controllers.ChessPiece

# Chess board class to set up initial state of the board and generate playable positions
from controllers import ChessPiece


class ChessBoard:
    positions = []

    def __init__(this):
        pass

    def setUp(this, whitePlayer, blackPlayer):
        # initialize board by creating playable fields
        for i in range(0,8):
            this.positions.append([])
            for j in range(0,8):
                this.positions[i].append(BoardSpot(i,j))
        
        # Place pieces in their original positions
        for i in range(0,8):
            this.positions[i][1].occupyField(ChessPiece.Pawn(whitePlayer))
            this.positions[i][6].occupyField(ChessPiece.Pawn(blackPlayer))

        this.positions[0][0].occupyField(ChessPiece.Rook(whitePlayer))
        this.positions[1][0].occupyField(ChessPiece.Knight(whitePlayer))
        this.positions[2][0].occupyField(ChessPiece.Bishop(whitePlayer))
        this.positions[3][0].occupyField(ChessPiece.Queen(whitePlayer))
        this.positions[4][0].occupyField(ChessPiece.King(whitePlayer))
        this.positions[5][0].occupyField(ChessPiece.Bishop(whitePlayer))
        this.positions[6][0].occupyField(ChessPiece.Knight(whitePlayer))
        this.positions[7][0].occupyField(ChessPiece.Rook(whitePlayer))

        this.positions[0][7].occupyField(ChessPiece.Rook(blackPlayer))
        this.positions[1][7].occupyField(ChessPiece.Knight(blackPlayer))
        this.positions[2][7].occupyField(ChessPiece.Bishop(blackPlayer))        
        this.positions[4][7].occupyField(ChessPiece.King(blackPlayer))
        this.positions[3][7].occupyField(ChessPiece.Queen(blackPlayer))
        this.positions[5][7].occupyField(ChessPiece.Bishop(blackPlayer))
        this.positions[6][7].occupyField(ChessPiece.Knight(blackPlayer))
        this.positions[7][7].occupyField(ChessPiece.Rook(blackPlayer))

        return this.positions

class BoardSpot():
    def __init__(this, xPosition, yPosition):
        this._xPos = xPosition
        this._yPos = yPosition
        this._occupant = None

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
