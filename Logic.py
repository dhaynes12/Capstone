from Board.py import Board
import Pieces as P

def select_piece(state, x, y):
    return state.board[x][y].validMoves(state, (x, y))
    
def move_piece(state, selX, selY, moveX, moveY):
    pass