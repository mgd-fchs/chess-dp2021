# Provide movement strategies to be implemented by ChessPiece

# imports
from abc import ABC


class MovementStrategy(ABC):
    def validateMove(originSpot, destinationSpot):
        pass


class SingleForward(MovementStrategy):
    # implemented by pawn

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        
        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove
        
        # check correct movement
        if originSpot.getOccupant().getColor() == "white":
            if originSpot.getPosition()[1] == destinationSpot.getPosition()[1] - 1:
                if originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
                    validMove = True
        elif originSpot.getOccupant().getColor() == "black":
            if originSpot.getPosition()[1] == destinationSpot.getPosition()[1] + 1:
                if originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
                    validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().getColor() == originSpot.getOccupant().getColor():
                validMove = False
        return validMove

class DoubleForward(MovementStrategy):
    # implemented by pawn (first move can be double)

    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        castleMove = False

        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove

        if originSpot.getPosition()[0] != originSpot.getPosition()[0]:
            validMove = False
            return validMove

        if destinationSpot.getOccupant():
            validMove = False

        xPos = originSpot.getPosition()[0]

        if originSpot.getOccupant().getColor() == "white":
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

        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove

        # check correct movement
        if originSpot.getPosition()[1] == destinationSpot.getPosition()[1]:
            # check path is free
            start = originSpot.getPosition()[0] + 1
            end = destinationSpot.getPosition()[0]
            y_coordinate = originSpot.getPosition()[1]

            for i in range(start, end):
                if game.board[i][y_coordinate].getOccupant():
                    print(str(game.board[i][y_coordinate].getOccupant()))
                    print(str(game.board[i][y_coordinate].getPosition()))
                    validMove = False
                    return validMove

            validMove = True
        
        elif originSpot.getPosition()[0] == destinationSpot.getPosition()[0]:
            start = originSpot.getPosition()[1] + 1
            end = destinationSpot.getPosition()[1]

            start = originSpot.getPosition()[1] + 1 
            end = destinationSpot.getPosition()[1]
            x_coordinate = originSpot.getPosition()[0]

            for i in range(start, end):
                if game.board[i][x_coordinate].getOccupant():
                    validMove = False
                    return validMove
            validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().getColor() == originSpot.getOccupant().getColor():
                validMove = False
        
        return validMove


class MultipleDiagonal(MovementStrategy):
    # implemented by bishop, queen
    
    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False

        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove       
            
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        # check correct movement
        if xDiff == yDiff:
            validMove = True
            
        xStart = originSpot.getPosition()[0] + 1
        xEnd = destinationSpot.getPosition()[0]

        yStart = originSpot.getPosition()[1] + 1
        yEnd = destinationSpot.getPosition()[1]

        for xPos in range(xStart, xEnd):
            for yPos in range(originSpot.getPosition()[1] + 1, destinationSpot.getPosition()[1]):
                if game.board[xPos][yPos].getOccupant():
                    validMove = False
                    return validMove

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().getColor() == originSpot.getOccupant().getColor():
                validMove = False

        return validMove


class SingleDiagonal(MovementStrategy):
    # implemented by king

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False

        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove
        
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])

        if (xDiff == 1 and yDiff == 1):
            validMove = True
        
        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().getColor() == originSpot.getOccupant().getColor():
                validMove = False

        return validMove


class SingleDiagonalForward(MovementStrategy):
    # implemented by pawn

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        
        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove
        
        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = originSpot.getPosition()[1] - destinationSpot.getPosition()[1]
        color = originSpot.getOccupant().getColor()

        if xDiff == 1:
            if color == "white" and yDiff == -1:
                if destinationSpot.getOccupant():
                    validMove = True
                elif destinationSpot.getPassant():
                    validMove = True
                    # handle en passant moves
                    if (not destinationSpot.getOccupant()):
                        hitFigureSpot = game.board[destinationSpot.getPosition()[0]][destinationSpot.getPosition()[1]-1]
                        hitFigureSpot.freeField()
                        validMove = True

            elif color == "black" and yDiff == 1:
                if destinationSpot.getOccupant():
                    validMove = True
                elif destinationSpot.getPassant():
                    # handle en passant moves
                    if (not destinationSpot.getOccupant()):
                        hitFigureSpot = game.board[destinationSpot.getPosition()[0]][destinationSpot.getPosition()[1]+1]
                        hitFigureSpot.freeField()                    
                        validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
           if destinationSpot.getOccupant().getColor() == originSpot.getOccupant().getColor():
               validMove = False

        return validMove


class TJump(MovementStrategy):
    # implemented by rook, king

    # overwrite validateMove() method
    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        
        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove

        xDiff = abs(originSpot.getPosition()[0] - destinationSpot.getPosition()[0])
        yDiff = abs(originSpot.getPosition()[1] - destinationSpot.getPosition()[1])      

        if xDiff == 2:
            if yDiff == 1:
                validMove = True
        elif yDiff == 2:
            if xDiff == 1:
                validMove = True

        # cannot replace figures of same color
        if destinationSpot.getOccupant():
            if destinationSpot.getOccupant().getColor() == originSpot.getOccupant().getColor():
                validMove = False
        return validMove

class CastleQueenside(MovementStrategy):

    def validateMove(game, originSpot, destinationSpot):
        validMove = False
        
        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove       
        
        if destinationSpot.getPosition()[0] != originSpot.getPosition()[0] - 2:
            validMove = False
            return validMove, False
        
        if game.getActivePlayer().queenCastle == True:
            print("Castling condition met")
            
            if game.getActivePlayer().getColor() == "white":
                for i in range(1,4):
                    spot = game.board[i][0]
                    if not spot.getOccupant():
                        validMove = True
            
            if game.getActivePlayer().getColor() == "black":
                for i in range(1,4):
                    spot = game.board[i][7]
                    if not spot.getOccupant():
                        validMove = True

            return validMove, "q"
        
class CastleKingside(MovementStrategy):

    def validateMove(game, originSpot, destinationSpot):
        validMove = False

        if not originSpot.getOccupant():
            print("Cannot move piece from empty spot!")
            return validMove

        if destinationSpot.getPosition()[0] != originSpot.getPosition()[0] + 2:
            validMove = False
            return validMove, False

        if game.getActivePlayer().kingCastle == True:
            print("Castling condition met")
            
            if game.getActivePlayer().getColor() == "white":
                for i in range(5,7): 
                    spot = game.board[i][0]
                    if not spot.getOccupant():
                        validMove = True

            if game.getActivePlayer().getColor() == "black":
                for i in range(5,7): 
                    spot = game.board[i][7]
                    if not spot.getOccupant():
                        validMove = True

        return validMove, "k"
