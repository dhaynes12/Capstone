import pytest
import Board as B
import Pieces as P
from copy import deepcopy

def compareMoveLists(moves1, moves2):
    if (len(moves1) != len(moves2)):
        return False

    # For each object in moves1, it removes an equal object in moves2.
    # If moves2 is empty, then the move lists are equal.
    for move1 in moves1:
        found = False
        for move2 in moves2:
            if move1 == move2:
                moves2.remove(move2)
                found = True
                break
        
        if not found:
            break
    
    return len(moves2) == 0

board = B.Board(True)


"""------------PAWN TESTS----------"""

pawnStart = deepcopy(board)
pawnStart.board[1][1] = P.Pawn(0, P.WHITE)

pawnStartBlocked1 = deepcopy(pawnStart)
pawnStartBlocked1.board[1][2] = P.Pawn(1, P.BLACK)
pawnStartBlocked1.unmoved.remove(1)

pawnStartBlocked2 = deepcopy(pawnStart)
pawnStartBlocked2.board[1][3] = P.Pawn(1, P.BLACK)
pawnStartBlocked2.unmoved.remove(1)

pawnCaptureAndPassent = deepcopy(board)
pawnCaptureAndPassent.board[4][4] = P.Pawn(0, P.WHITE)
pawnCaptureAndPassent.board[3][4] = P.Pawn(1, P.BLACK)
pawnCaptureAndPassent.board[5][5] = P.Pawn(2, P.BLACK)
pawnCaptureAndPassent.passentable = (3, 4)
pawnCaptureAndPassent.unmoved.remove(0)
pawnCaptureAndPassent.unmoved.remove(1)
pawnCaptureAndPassent.unmoved.remove(2)

pawnStartBlack = deepcopy(board)
pawnStartBlack.board[6][6] = P.Pawn(0, P.BLACK)

pawnCPBlack= deepcopy(board)
pawnCPBlack.board[4][3] = P.Pawn(0, P.BLACK)
pawnCPBlack.board[3][3] = P.Pawn(1, P.WHITE)
pawnCPBlack.board[5][2] = P.Pawn(2, P.WHITE)
pawnCPBlack.passentable = (3, 3)
pawnCPBlack.unmoved.remove(0)
pawnCPBlack.unmoved.remove(1)
pawnCPBlack.unmoved.remove(2)


pawnStartMoves = [
                    P.Move((1,2), P.NON_CAPTURE),
                    P.Move((1,3), P.NON_CAPTURE)
                 ]
pSB1Moves = []
pSB2Moves = [P.Move((1,2), P.NON_CAPTURE)]
pCPMoves = [
                P.Move((4,5), P.NON_CAPTURE),
                P.Move((3,5), P.EN_PASSENT),
                P.Move((5,5))
           ]
pawnStartBlackMoves = [
                    P.Move((6,5), P.NON_CAPTURE),
                    P.Move((6,4), P.NON_CAPTURE)
                 ]
pCPBMoves = [
                P.Move((4,2), P.NON_CAPTURE),
                P.Move((3,2), P.EN_PASSENT),
                P.Move((5,2))
           ]


"""------------KNIGHT TESTS----------"""
knightCenter = deepcopy(board)
knightCenter.board[3][3] = P.Knight(0, P.WHITE)
knightCenter.unmoved.remove(0)

knightCenter2 = deepcopy(knightCenter)
knightCenter2.board[2][1] = P.Pawn(1, P.WHITE)
knightCenter2.board[5][4] = P.Knight(2, P.WHITE)
knightCenter2.board[1][2] = P.Queen(3, P.BLACK)
knightCenter2.board[4][1] = P.Bishop(4, P.BLACK)
knightCenter2.unmoved.remove(2)
knightCenter2.unmoved.remove(3)
knightCenter2.unmoved.remove(4)

knightCorner = deepcopy(board)
knightCorner.board[0][7] = P.Knight(0, P.BLACK)
knightCorner.unmoved.remove(0)


knCMoves = [
            P.Move((2,1)),
            P.Move((4,1)),
            P.Move((5,2)),
            P.Move((5,4)),
            P.Move((4,5)),
            P.Move((2,5)),
            P.Move((1,4)),
            P.Move((1,2))
          ]

knC2Moves = [
            P.Move((4,1)),
            P.Move((5,2)),
            P.Move((4,5)),
            P.Move((2,5)),
            P.Move((1,4)),
            P.Move((1,2))
          ]

knCornerMoves = [
                P.Move((1,5)),
                P.Move((2,6))
               ]


"""------------BISHOP TESTS----------"""
bishopCenter = deepcopy(board)
bishopCenter.board[5][4] = P.Bishop(0, P.WHITE)
bishopCenter.unmoved.remove(0)

bishopCenter2 = deepcopy(bishopCenter)
bishopCenter2.board[3][2] = P.Queen(1, P.BLACK)
bishopCenter2.board[4][5] = P.Queen(2, P.WHITE)
bishopCenter2.unmoved.remove(1)
bishopCenter2.unmoved.remove(2)

bCMoves = [
            P.Move((1,0)),
            P.Move((2,1)),
            P.Move((3,2)),
            P.Move((4,3)),
            P.Move((2,7)),
            P.Move((3,6)),
            P.Move((4,5)),
            P.Move((7,6)),
            P.Move((6,5)),
            P.Move((6,3)),
            P.Move((7,2))
          ]

bC2Moves = [
            P.Move((3,2)),
            P.Move((4,3)),
            P.Move((7,6)),
            P.Move((6,5)),
            P.Move((6,3)),
            P.Move((7,2))
          ]


"""------------ROOK TESTS----------"""
rookCenter = deepcopy(board)
rookCenter.board[3][3] = P.Rook(0, P.WHITE)
rookCenter.unmoved.remove(0)

rookCenter2 = deepcopy(rookCenter)
rookCenter2.board[2][3] = P.Pawn(1, P.WHITE)
rookCenter2.board[3][1] = P.Pawn(2, P.WHITE)
rookCenter2.board[3][4] = P.Pawn(3, P.BLACK)
rookCenter2.board[5][3] = P.Pawn(4, P.BLACK)
rookCenter2.unmoved.remove(1)
rookCenter2.unmoved.remove(3)
rookCenter2.unmoved.remove(4)

rCMoves = [
            P.Move((0,3)),
            P.Move((1,3)),
            P.Move((2,3)),
            P.Move((4,3)),
            P.Move((5,3)),
            P.Move((6,3)),
            P.Move((7,3)),
            P.Move((3,0)),
            P.Move((3,1)),
            P.Move((3,2)),
            P.Move((3,4)),
            P.Move((3,5)),
            P.Move((3,6)),
            P.Move((3,7))
          ]

rC2Moves = [
            P.Move((4,3)),
            P.Move((5,3)),
            P.Move((3,2)),
            P.Move((3,4))
          ]


"""------------QUEEN TESTS----------"""
queenCenter = deepcopy(board)
queenCenter.board[3][3] = P.Queen(0, P.WHITE)
queenCenter.board[2][3] = P.Pawn(1, P.WHITE)
queenCenter.board[3][1] = P.Pawn(2, P.WHITE)
queenCenter.board[1][1] = P.Pawn(3, P.WHITE)
queenCenter.board[2][4] = P.Pawn(4, P.WHITE)
queenCenter.board[3][4] = P.Pawn(5, P.BLACK)
queenCenter.board[5][3] = P.Pawn(6, P.BLACK)
queenCenter.board[4][2] = P.Pawn(7, P.BLACK)
queenCenter.board[5][5] = P.Pawn(8, P.BLACK)
queenCenter.unmoved.remove(0)
queenCenter.unmoved.remove(1)
queenCenter.unmoved.remove(4)
queenCenter.unmoved.remove(5)
queenCenter.unmoved.remove(6)
queenCenter.unmoved.remove(7)
queenCenter.unmoved.remove(8)

qCMoves = [
            P.Move((4,3)),
            P.Move((5,3)),
            P.Move((3,2)),
            P.Move((3,4)),
            P.Move((2,2)),
            P.Move((4,2)),
            P.Move((4,4)),
            P.Move((5,5))
          ]


"""------------KING TESTS----------"""
kingCenter = deepcopy(board)
kingCenter.board[3][3] = P.King(0, P.WHITE)
kingCenter.unmoved.remove(0)

kingCastle = deepcopy(board)
kingCastle.board[4][0] = P.King(0, P.WHITE)
kingCastle.board[0][0] = P.Rook(1, P.WHITE)
kingCastle.board[7][0] = P.Rook(2, P.WHITE)

kingCastleOpposed = deepcopy(kingCastle)
kingCastleOpposed.board[3][1] = P.Pawn(3, P.BLACK)
kingCastleOpposed.whiteChecked = True
kingCastleOpposed.unmoved.remove(3)

kingCastleOpposed2 = deepcopy(kingCastle)
kingCastleOpposed2.board[3][1] = P.Rook(3, P.BLACK)
kingCastleOpposed2.unmoved.remove(3)

kingCastleOpposed3 = deepcopy(kingCastle)
kingCastleOpposed3.board[3][0] = P.Queen(3, P.WHITE)
kingCastleOpposed3.board[5][0] = P.Knight(4, P.WHITE)

kCenterMoves = [
            P.Move((4,3)),
            P.Move((4,2)),
            P.Move((3,2)),
            P.Move((2,2)),
            P.Move((2,3)),
            P.Move((2,4)),
            P.Move((3,4)),
            P.Move((4,4))
          ]

kCastleMoves = [
                   P.Move((4,1)),
                   P.Move((5,1)),
                   P.Move((5,0)),
                   P.Move((3,0)),
                   P.Move((3,1)),
                   P.Move((2,0), P.CASTLE),
                   P.Move((6,0), P.CASTLE)
               ]

kCOMoves = [
                   P.Move((4,1)),
                   P.Move((5,1)),
                   P.Move((5,0)),
                   P.Move((3,0)),
                   P.Move((3,1))
           ]
 
kCO2Moves = [
                   P.Move((4,1)),
                   P.Move((5,1)),
                   P.Move((5,0)),
                   P.Move((3,0)),
                   P.Move((3,1)),
                   P.Move((6,0), P.CASTLE)
            ]

kCO3Moves = [
                   P.Move((4,1)),
                   P.Move((5,1)),
                   P.Move((3,1))
            ]


@pytest.mark.parametrize(
    "b,tX,tY,expectedMoves,n",
    [
        (pawnStart, 1, 1, pawnStartMoves, 1),
        (pawnStartBlocked1, 1, 1, pSB1Moves, 2),
        (pawnStartBlocked2, 1, 1, pSB2Moves, 3),
        (pawnCaptureAndPassent, 4, 4, pCPMoves, 4),
        (pawnStartBlack, 6, 6, pawnStartBlackMoves, 5),
        (pawnCPBlack, 4, 3, pCPBMoves, 6),
        (knightCenter, 3, 3, knCMoves, 7),
        (knightCenter2, 3, 3, knC2Moves, 8),
        (knightCorner, 0, 7, knCornerMoves, 9),
        (bishopCenter, 5, 4, bCMoves, 10),
        (bishopCenter2, 5, 4, bC2Moves, 11),
        (rookCenter, 3, 3, rCMoves, 12),
        (rookCenter2, 3, 3, rC2Moves, 13),
        (queenCenter, 3, 3, qCMoves, 14),
        (kingCenter, 3, 3, kCenterMoves, 15),
        (kingCastle, 4, 0, kCastleMoves, 16),
        (kingCastleOpposed, 4, 0, kCOMoves, 17),
        (kingCastleOpposed2, 4, 0, kCO2Moves, 18),
        (kingCastleOpposed3, 4, 0, kCO3Moves, 19)
    ]
)
def test_move(b, tX, tY, expectedMoves, n):
    #pytest.set_trace()
    moves = b.board[tX][tY].validMoves(b, (tX, tY))
    assert n == n and compareMoveLists(moves, expectedMoves) == True