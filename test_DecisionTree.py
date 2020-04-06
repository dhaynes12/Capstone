import pytest
import Board as B
import Pieces as P
import Logic
from DecisionTree import aiSearch, endStateCheck, Node

stalemate = B.Board(True)

stalemate.board[3][3] = P.King(stalemate.whiteKingId, P.WHITE)
stalemate.board[0][4] = P.Rook(100, P.BLACK)
stalemate.board[2][0] = P.Queen(101, P.BLACK)
stalemate.board[5][1] = P.Knight(102, P.BLACK)
stalemate.board[7][2] = P.Rook(103, P.BLACK)
stalemate.board[7][7] = P.King(stalemate.blackKingId, P.BLACK)
stalemate.unmoved = []

unknownError = B.Board()
Logic.move_piece(unknownError, 4, 1, P.Move((4,3), P.NON_CAPTURE))
Logic.move_piece(unknownError, 6, 6, P.Move((6,4), P.NON_CAPTURE))
Logic.move_piece(unknownError, 3, 0, P.Move((5,2)))
Logic.move_piece(unknownError, 5, 7, P.Move((6,6)))
Logic.move_piece(unknownError, 5, 0, P.Move((2,3)))

@pytest.mark.parametrize(
    "state,depthLim,heuristic",
    [
        (stalemate, 1, 0)
    ]
)
def test_move_return(state, depthLim,heuristic):
    aiSearch(state, depthLim,heuristic)
    assert 1

@pytest.mark.parametrize(
    "state,depthLim,heuristic",
    [
        (unknownError, 3, 0)
    ]
)
def test_tree_gen(state, depthLim, heuristic):
    def tree_gen(node):
        if (node.depth < node.depthLim):
            node.genNextMoves()
            if (len(node.nextMoves) == 0):
                endStateCheck(node, None)
            else:
                for n in (node.nextMoves):
                    tree_gen(n)
    
    tempNode = Node(state.turn, state, 0, depthLim, heuristic)
    tree_gen(tempNode)
    assert 1