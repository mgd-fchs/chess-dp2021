# import ChessPieces
# class to represent each field on the chessboard


class BoardSpot():
    """  
    state: occupied (by who?) or not
    position (x, y) + translation of y to letters
    """
    def __init__(this, xPosition, yPosition):
        _xPos = xPosition
        _yPos = yPosition
        _occupant = None

    def occupyField(this, chessPiece):
        this._occupant = chessPiece
        # notify logger here or in main class?

    def freeField(this):
        this._occupant = None

    def getPosition(this):
        # getter function for coordinates
        
        position = tuple(_xPos, _yPos)
        return position

# use state pattern?