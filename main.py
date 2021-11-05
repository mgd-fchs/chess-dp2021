# imports
from Game import Game

def main():
    newGame = Game()

    # simple testing calls, to be deleted
    originSpot = newGame.board[0][1]
    destinationSpot = newGame.board[0][2]

    # valid move
    newGame.executeMove(originSpot, destinationSpot)
    """ expected output: 
        This is a valid move!
        Moving piece x to coordinates
    """

    # valid move but wrong player
    newGame.executeMove(destinationSpot, newGame.board[0][3])
    """ expected output: 
        This is a valid move!
        Cannot make move, it's not your turn
    """

    # correct player but invalid move
    newGame.executeMove(newGame.board[0][6], newGame.board[0][7])
    """ expected output: 
        Please select a valid move!
    """

if __name__ == "__main__":
    main()