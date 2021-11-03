# imports
from ChessBoard import ChessBoard
import ChessPiece

### simple testing calls, replace with actual interface, gameflow
chessBoard = ChessBoard().setUp("whitePlayer", "blackPlayer") # TODO: replace with actual player instances

Pawn = ChessPiece.Pawn("somePlayer", "someSymbol")
Pawn.move(chessBoard[0][1])

# test if after setup, every board spot knows its occupant

# TODO: initialize player
# TODO: set initial state for each player
# TODO: how to control game from here? Possibility: Each move is logged anyway -> use logged info to determine winning condition?
# Or check consequence at the end of every move (that is, method executed in player state...execution of a move could be in separate class and 
# only called by the player state)