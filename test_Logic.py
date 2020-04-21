import pytest
import Board as B
import Pieces as P
import Logic

testCase1 = B.Board()
testCase1 = Logic.move_piece(testCase1, 4, 1, P.Move((4,3), P.NON_CAPTURE))
testCase1 = Logic.move_piece(testCase1, 2, 6, P.Move((2,5), P.NON_CAPTURE))
testCase1 = Logic.move_piece(testCase1, 5, 1, P.Move((5,3), P.NON_CAPTURE))
testCase1 = Logic.move_piece(testCase1, 3, 6, P.Move((3,5), P.NON_CAPTURE))
testCase1 = Logic.move_piece(testCase1, 6, 1, P.Move((6,3), P.NON_CAPTURE))
testCase1 = Logic.move_piece(testCase1, 4, 6, P.Move((3,4), P.NON_CAPTURE))
testCase1 = Logic.move_piece(testCase1, 6, 0, P.Move((4,1)))
testCase1 = Logic.move_piece(testCase1, 3, 7, P.Move((7,3)))

testCase2 = B.Board()
testCase2 = Logic.move_piece(testCase2, 0, 1, P.Move((0,3), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 4, 6, P.Move((4,4), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 1, 1, P.Move((1,3), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 7, 6, P.Move((7,4), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 2, 1, P.Move((2,3), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 3, 7, P.Move((5,5)))
testCase2 = Logic.move_piece(testCase2, 0, 3, P.Move((0,4), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 7, 7, P.Move((7,5)))
testCase2 = Logic.move_piece(testCase2, 1, 3, P.Move((1,4), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 5, 5, P.Move((5,4)))
testCase2 = Logic.move_piece(testCase2, 2, 3, P.Move((2,4), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 7, 5, P.Move((5,5)))
testCase2 = Logic.move_piece(testCase2, 0, 4, P.Move((0,5), P.NON_CAPTURE))
testCase2 = Logic.move_piece(testCase2, 5, 4, P.Move((5,1)))

testCase3 = B.Board()
testCase3 = Logic.move_piece(testCase3, 4, 1, P.Move((4,3), P.NON_CAPTURE))
testCase3 = Logic.move_piece(testCase3, 0, 6, P.Move((0,4), P.NON_CAPTURE))
testCase3 = Logic.move_piece(testCase3, 3, 0, P.Move((5,2)))
testCase3 = Logic.move_piece(testCase3, 1, 6, P.Move((1,4), P.NON_CAPTURE))
testCase3 = Logic.move_piece(testCase3, 5, 0, P.Move((2,3)))
testCase3 = Logic.move_piece(testCase3, 1, 4, P.Move((1,3), P.NON_CAPTURE))
testCase3 = Logic.move_piece(testCase3, 5, 2, P.Move((5,6)))

testCase4 = B.Board(True)
testCase4.board[0][0] = P.King(testCase4.whiteKingId, P.WHITE)
testCase4.board[1][0] = P.Rook(100, P.WHITE)
testCase4.board[2][0] = P.Rook(101, P.WHITE)
testCase4.board[2][1] = P.Queen(102, P.BLACK)
testCase4.board[7][1] = P.Pawn(103, P.WHITE)
testCase4.board[0][2] = P.Pawn(104, P.WHITE)
testCase4.board[1][2] = P.Knight(105, P.BLACK)
testCase4.board[2][3] = P.Knight(106, P.BLACK)
testCase4.board[4][5] = P.Pawn(107, P.BLACK)
testCase4.board[1][6] = P.Pawn(108, P.BLACK)
testCase4.board[6][6] = P.Pawn(109, P.BLACK)
testCase4.board[7][6] = P.Pawn(110, P.BLACK)
testCase4.board[2][7] = P.Bishop(111, P.BLACK)
testCase4.board[3][7] = P.Rook(112, P.BLACK)
testCase4.board[6][7] = P.King(testCase4.blackKingId, P.BLACK)
testCase4.unmoved = [103, 108, 109, 110, 111]
testCase4.initializePosVals()

@pytest.mark.parametrize(
    "b,color,expectedAnswer",
    [
        (testCase4, P.WHITE, False),
        (testCase1, P.WHITE, False),
        (testCase2, P.WHITE, True),
        (testCase3, P.BLACK, True)
    ]
)
def test_is_checkmate(b, color, expectedAnswer):
    #pytest.set_trace()
    assert Logic.is_checkmate(b, color) == expectedAnswer