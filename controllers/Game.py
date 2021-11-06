# Composite class

from controllers.Player import Player
from controllers.ChessBoard import ChessBoard

class Game():

    def __init__(this):
        # instantiate players
        this.whitePlayer = Player("white")
        this.blackPlayer = Player("black")

        # instantiate board
        this.board = ChessBoard().setUp(this.whitePlayer, this.blackPlayer)

        # TODO: Instantiate other components: e.g. History
  
  
    def executeMove(this, originSpot, destinationSpot):
        # TODO: Link to calls from GUI (?)
        piece = originSpot.getOccupant()

        if not piece:
            print("Cannot move piece from empty spot")
            return
        
        player = piece.player

        valid = False
        for strategy in piece.movementStrategy:
            valid = strategy.validateMove(this, originSpot, destinationSpot)
            if valid == True:
                print("This is a valid move!")
                break

        if valid == False:
            print("Please select a valid move!")
            return

        player.makeMove(originSpot, destinationSpot)

        # TODO: Ensure there is no other figure in the way -> Should be in Strategy.validate()
        # TODO: Check player state before validity of move (also possibly switch move execution from Player to Game)
        # TODO: Implement castling (history needed!)
        # TODO: Replace print statements with prioper messages/warnings

    def end(this):
        # to be called when a player wins or gives up
        # ends the application
        pass

    def undo(this):
        # TODO
        pass

    def redo(this):
        # TODO
        pass

    def reset(this):
        # TODO
        pass

    def replay(this):
        # TODO
        pass