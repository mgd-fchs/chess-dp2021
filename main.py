# imports
from ChessBoard import ChessBoard
from Player import Player

def main():
    # simple testing calls, to be replaced 

    whitePlayer = Player("white")
    blackPlayer = Player("black")

    chessBoard = ChessBoard().setUp(whitePlayer, blackPlayer)

    # chessBoard[5][7].getOccupant()
    # chessBoard[5][7].getOccupant().move(chessBoard[5,7],chessBoard[4][4])

    whitePlayer.makeMove(chessBoard[0][1], chessBoard[0][2])
    blackPlayer.makeMove(chessBoard[2][5], chessBoard[2][4])
    blackPlayer.makeMove(chessBoard[2][5], chessBoard[2][4])
    blackPlayer.makeMove(chessBoard[2][5], chessBoard[2][4])
    whitePlayer.makeMove(chessBoard[0][2], chessBoard[0][3])

if __name__ == "__main__":
    main()