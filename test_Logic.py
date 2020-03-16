import pytest
import Pieces as P
import Board as B
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


@pytest.mark.parametrize(
    "b,color,expectedAnswer",
    [
        (testCase1, P.WHITE, False),
        (testCase2, P.WHITE, True)
    ]
)
def test_is_checkmate(b, color, expectedAnswer):
    assert Logic.is_checkmate(b, color) == expectedAnswer