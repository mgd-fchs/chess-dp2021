# imports
from ChessBoard import ChessBoard
import ChessPiece

### simple testing calls, replace with actual interface, gameflow
chessBoard = ChessBoard().setUp()

Pawn = ChessPiece.Pawn(chessBoard[0][0], "", "")
Pawn.move(chessBoard[0][1])

# TODO: initialize player
# TODO: set initial state for each player
# TODO: how to control game from here?