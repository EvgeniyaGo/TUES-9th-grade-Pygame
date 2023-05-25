#Store all info about what's going on.

class GameState():
    def __init__(self):
        self.board = [["--","--","--","--","--"], #the board 5x5
                      ["--","--","--","--","--"], #BN - Bunny, the player
                      ["--","--","BN","--","--"], #-- - empty
                      ["--","--","--","--","--"],
                      ["--","--","--","--","--"]]
        self.you_move = True
        self.moveLog = []
