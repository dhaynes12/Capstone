import pytest
import Board as B
import Pieces as P
import Logic
from DecisionTree import aiSearch

stalemate = B.Board(True)

stalemate.board[3][3] = P.King(stalemate.whiteKingId, P.WHITE)
stalemate.board[0][4] = P.Rook(100, P.BLACK)
stalemate.board[2][0] = P.Queen(101, P.BLACK)
stalemate.board[5][1] = P.Knight(102, P.BLACK)
stalemate.board[7][2] = P.Rook(103, P.BLACK)
stalemate.board[7][7] = P.King(stalemate.blackKingId, P.BLACK)
stalemate.unmoved = []

@pytest.mark.parametrize(
    "state,depthLim",
    [
        (stalemate, 1)
    ]
)
def test_move_return(state, depthLim):
    aiSearch(state, depthLim)
    assert 1