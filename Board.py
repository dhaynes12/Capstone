import Pieces as P

class Board():
    def __init__(self):
        self.board = []             # The game's current state, represented as a 2d array of Piece and Empty objects
        self.prevBoard = []         # The game's previous state
        self.whiteChecked = False   # True when white's king is in check
        self.blackChecked = False   # True when black's king is in check