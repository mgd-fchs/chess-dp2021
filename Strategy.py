from abc import ABC, abstractmethod

class MovementStrategy(ABC):
    def validateMove(originSpot, destinationSpot):
        pass

class SingleForward(MovementStrategy):
    # implemented by pawn

    # overwrite validateMove() method
    def validateMove(originSpot, destinationSpot):
        validMove = False
        if originSpot.getOccupant().color == "white":
            if originSpot.getPosition()[1] == destinationSpot.getPosition()[1]-1:
                if originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
                    validMove = True
        elif originSpot.getOccupant().color == "black":
            if originSpot.getPosition()[1] == destinationSpot.getPosition()[1]+1:
                if originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
                    validMove = True

        return validMove


class MultipleStraight(MovementStrategy):
    # implemented by rook, queen

    # overwrite validateMove() method
    def validateMove(originSpot, destinationSpot):
        validMove = False
        if originSpot.getPosition()[1] == destinationSpot.getPosition()[1]:
            validMove = True
        elif originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
            validMove = True
        
        return validMove

class MultipleDiagonal(MovementStrategy):
    # implemented by bishop, queen

    # overwrite validateMove() method
    def validateMove(originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        validMove = False
        if xDiff == yDiff:
            validMove = True
        
        return validMove

class SingleDiagonal(MovementStrategy):
    # implemented by king

    # overwrite validateMove() method
    def validateMove(this, originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        validMove = False
        if (xDiff == 1 and yDiff == 1):
            validMove = True
        
        return validMove

class SingleDiagonalForward(MovementStrategy):
    # implemented by pawn

    # overwrite validateMove() method
    def validateMove(originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = originSpot.getPosition()[1] - destinationSpot.getPosition()[1]
        color = originSpot.getOccupant().color

        validMove = False
        if xDiff == 1:
            if destinationSpot.getOccupant():
                if color == "white" and yDiff == -1:
                    validMove = True
                elif color == "black" and yDiff == 1:
                    validMove = True
        
        return validMove

class TJump(MovementStrategy):
    # implemented by rook, king

    # overwrite validateMove() method
    def validateMove(originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        validMove = False

        if xDiff == 2:
            if yDiff == 1:
                validMove = True
        elif yDiff == 2:
            if xDiff == 1:
                validMove = True
        
        return validMove