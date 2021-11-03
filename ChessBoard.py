# imports
from BoardSpot import BoardSpot
import numpy

# chess board class to set up initial state of the board and generate playable positions

class ChessBoard:
    positions = []

    def __init__(this):
        pass

    def setUp(this):
        # initialize board by creating playable fields
        for i in range(0,8):
            this.positions.append([])
            for j in range(0,8):
                this.positions[i].append(BoardSpot(i, j))
                # link to GUI object?
        
        return this.positions
        # TODO: place pieces in initial positions
        # boardMatrix[0,0].occupyField(Rook etc.)
        # print(this.boardMatrix)



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

# Alt1: Board spot knows its occupant, occupant knows its player, the player has a colour
# probably better because easier to manage (move "x" from K4 to K6 -> query by field not by figure)
# Alt2: Figure knows its position