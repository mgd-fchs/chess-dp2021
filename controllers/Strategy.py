from abc import ABC, abstractmethod


class MovementStrategy(ABC):
    def validateMove(originSpot, destinationSpot):
        pass


class SingleForward(MovementStrategy):
    # implemented by pawn

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        # check correct movement
        if originSpot.getOccupant().color == "white":
            if originSpot.getPosition()[1] == destinationSpot.getPosition()[1] - 1:
                if originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
                    validMove = True
        elif originSpot.getOccupant().color == "black":
            if originSpot.getPosition()[1] == destinationSpot.getPosition()[1] + 1:
                if originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
                    validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().color == originSpot.getOccupant().color:
                validMove = False
        return validMove

class DoubleForward(MovementStrategy):
    # implemented by pawn (first move can be double)

    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        
        if originSpot.getPosition()[0] != originSpot.getPosition()[0]:
            validMove = False
            return validMove

        if destinationSpot.getOccupant():
            validMove = False

        xPos = originSpot.getPosition()[0]

        if originSpot.getOccupant().color == "white":
            if originSpot.getPosition()[1] == 1:
                if destinationSpot.getPosition()[1] == 3:
                    # set en passant option
                    game.board[xPos][2].setPassant()
                    validMove = True
        else:
            if originSpot.getPosition()[1] == 6:
                if destinationSpot.getPosition()[1] == 4:
                    # set en passant option
                    game.board[xPos][5].setPassant()
                    validMove = True

        return validMove

class MultipleStraight(MovementStrategy):
    # implemented by rook, queen

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False

        # check correct movement
        if originSpot.getPosition()[1] == destinationSpot.getPosition()[1]:
            # check path is free
            start = originSpot.getPosition()[0]
            end = destinationSpot.getPosition()[0]
            y_coordinate = originSpot.getPosition()[1]
            
            for i in range(start, end):
                if game.board[i][y_coordinate].getOccupant():
                    validMove = False
                    return validMove
            validMove = True
        
        elif originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
            start = originSpot.getPosition()[1]
            end = destinationSpot.getPosition()[1]
            x_coordinate = originSpot.getPosition()[1]

            for i in range(start, end):
                if game.board[i][x_coordinate].getOccupant():
                    validMove = False
                    return validMove
            validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().color == originSpot.getOccupant().color:
                validMove = False
        
        return validMove


class MultipleDiagonal(MovementStrategy):
    # implemented by bishop, queen

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        validMove = False
        
        # check correct movement
        if xDiff == yDiff:
            validMove = True

        for xPos in range(originSpot.getPosition()[0], destinationSpot.getPosition()[0]):
            for yPos in range(originSpot.getPosition()[1], destinationSpot.getPosition()[1]):
                if game.board[xPos][yPos].getOccupant():
                    validMove = False
                    return validMove

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().color == originSpot.getOccupant().color:
                validMove = False

        return validMove


class SingleDiagonal(MovementStrategy):
    # implemented by king

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        validMove = False
        if (xDiff == 1 and yDiff == 1):
            validMove = True
        
        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().color == originSpot.getOccupant().color:
                validMove = False

        return validMove


class SingleDiagonalForward(MovementStrategy):
    # implemented by pawn

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
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

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().color == originSpot.getOccupant().color:
                validMove = False

        return validMove


class TJump(MovementStrategy):
    # implemented by rook, king

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        validMove = False

        if xDiff == 2:
            if yDiff == 1:
                validMove = True
        elif yDiff == 2:
            if xDiff == 1:
                validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().color == originSpot.getOccupant().color:
                validMove = False
        return validMove
