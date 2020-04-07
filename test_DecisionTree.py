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
unknownError = Logic.move_piece(unknownError, 4, 1, P.Move((4,3), P.NON_CAPTURE))
unknownError = Logic.move_piece(unknownError, 6, 6, P.Move((6,4), P.NON_CAPTURE))
unknownError = Logic.move_piece(unknownError, 3, 0, P.Move((5,2)))
unknownError = Logic.move_piece(unknownError, 5, 7, P.Move((6,6)))
unknownError = Logic.move_piece(unknownError, 5, 0, P.Move((2,3)))
unknownError = Logic.move_piece(unknownError, 0, 6, P.Move((0,4), P.NON_CAPTURE))
unknownError = Logic.move_piece(unknownError, 5, 2, P.Move((5,6)))

crash = B.Board(True)
crash.board[5][0] = P.Bishop(100, P.WHITE)
crash.board[2][1] = P.Pawn(101, P.WHITE)
crash.board[4][1] = P.Pawn(102, P.WHITE)
crash.board[5][1] = P.King(crash.whiteKingId, P.WHITE)
crash.board[0][2] = P.Pawn(103, P.WHITE)
crash.board[2][2] = P.Pawn(104, P.WHITE)
crash.board[5][2] = P.Knight(105, P.WHITE)
crash.board[2][3] = P.Bishop(106, P.BLACK)
crash.board[3][3] = P.Rook(107, P.WHITE)
crash.board[4][3] = P.King(crash.blackKingId, P.BLACK)
crash.board[6][3] = P.Pawn(108, P.WHITE)
crash.board[0][4] = P.Pawn(109, P.BLACK)
crash.board[1][4] = P.Pawn(110, P.BLACK)
crash.board[6][4] = P.Pawn(111, P.WHITE)
crash.board[0][7] = P.Rook(112, P.BLACK)
crash.board[1][7] = P.Knight(113, P.BLACK)
crash.board[2][7] = P.Rook(114, P.WHITE)
crash.turn = P.BLACK
crash.blackChecked = True
crash.unmoved = [101, 102]

crash2 = B.Board(True)
crash2.board[0][1] = P.Knight(100, P.WHITE)
crash2.board[1][5] = P.Pawn(101, P.WHITE)
crash2.board[1][7] = P.King(crash2.blackKingId, P.BLACK)
crash2.board[2][1] = P.Pawn(102, P.WHITE)
crash2.board[2][5] = P.Queen(103, P.WHITE)
crash2.board[3][2] = P.Pawn(104, P.WHITE)
crash2.board[4][3] = P.Pawn(105, P.WHITE)
crash2.board[4][4] = P.Pawn(106, P.BLACK)
crash2.board[5][1] = P.King(crash2.whiteKingId, P.WHITE)
crash2.turn = P.BLACK
crash2.unmoved = [102]

crash3 = B.Board(True)
crash3.board[2][0] = P.King(crash3.whiteKingId, P.WHITE)
crash3.board[2][1] = P.Queen(100, P.BLACK)
crash3.board[3][1] = P.Rook(101, P.BLACK)
crash3.board[4][7] = P.King(crash3.blackKingId, P.BLACK)
crash3.board[5][3] = P.Queen(102, P.WHITE)
crash3.turn = P.WHITE
crash3.whiteChecked = True
crash2.unmoved = []

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
    "state,aicolor,depthLim,heuristic",
    [
        (crash3, P.WHITE, 3, 0),
        (crash2, P.BLACK, 3, 0),
        (crash, P.BLACK, 3, 0),
        (unknownError, P.BLACK, 3, 0)
    ]
)
def test_tree_gen(state, aicolor, depthLim, heuristic):
    def tree_gen(node):
        if (node.depth < node.depthLim):
            node.genNextMoves()
            if (len(node.nextMoves) == 0):
                endStateCheck(node, None)
            else:
                for n in (node.nextMoves):
                    tree_gen(n)
    
    
    #pytest.set_trace()
    tempNode = Node(aicolor, state, 0, depthLim, heuristic)
    tree_gen(tempNode)
    assert 1