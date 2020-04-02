import Pieces as P

W_ROOKS = [P.Rook(0, P.WHITE), P.Rook(5, P.WHITE)]
W_KNIGHTS = [P.Knight(1, P.WHITE), P.Knight(6, P.WHITE)]
W_BISHOPS = [P.Bishop(2, P.WHITE), P.Bishop(7, P.WHITE)]
W_QUEEN = P.Queen(3, P.WHITE)
W_KING = P.King(4, P.WHITE)
W_PAWNS = []

B_ROOKS = [P.Rook(8, P.BLACK), P.Rook(13, P.BLACK)]
B_KNIGHTS = [P.Knight(9, P.BLACK), P.Knight(14, P.BLACK)]
B_BISHOPS = [P.Bishop(10, P.BLACK), P.Bishop(15, P.BLACK)]
B_QUEEN = P.Queen(11, P.BLACK)
B_KING = P.King(12, P.BLACK)
B_PAWNS = []

EMPTY = P.Empty()

for i in range(0, 8):
    W_PAWNS.append(P.Pawn(16 + i, P.WHITE))
    B_PAWNS.append(P.Pawn(24 + i, P.BLACK))

class Board():

    def __init__(self, blank=False):
        self.board = []                     # The game's current state, represented as a 2d array of Piece and Empty objects
        self.unmoved = list(range(0, 32))   # The ids of all pieces that haven't moved
        self.whiteChecked = False           # True when white's king is in check
        self.blackChecked = False           # True when black's king is in check
        self.turn = P.WHITE
        self.whiteKingId = 4
        self.blackKingId = 12
        self.whiteTotalPieceVal = 0
        self.blackTotalPieceVal = 0
        self.passentable = None
        
        for x in range(0, 8):
            self.board.append([])
            for y in range(0, 8):
                self.board[x].append(EMPTY)
        
        if (not blank):
            self.board[0][0] = W_ROOKS[0]
            self.board[1][0] = W_KNIGHTS[0]
            self.board[2][0] = W_BISHOPS[0]
            self.board[3][0] = W_QUEEN
            self.board[4][0] = W_KING
            self.board[7][0] = W_ROOKS[1]
            self.board[6][0] = W_KNIGHTS[1]
            self.board[5][0] = W_BISHOPS[1]
            
            self.board[0][7] = B_ROOKS[0]
            self.board[1][7] = B_KNIGHTS[0]
            self.board[2][7] = B_BISHOPS[0]
            self.board[3][7] = B_QUEEN
            self.board[4][7] = B_KING
            self.board[7][7] = B_ROOKS[1]
            self.board[6][7] = B_KNIGHTS[1]
            self.board[5][7] = B_BISHOPS[1]
            
            for i in range(0, 8):
                self.board[i][1] = W_PAWNS[i]
                self.board[i][6] = B_PAWNS[i]
        
        pieces, loc = self.getAllPieces()
        for i in range(0, len(pieces)):
            if pieces[i].color == P.WHITE:
                self.whiteTotalPieceVal += pieces[i].value
                if pieces[i].value == P.PAWN_VAL:
                    self.whiteTotalPieceVal += P.WHT_PAWN_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.ROOK_VAL:
                    self.whiteTotalPieceVal += P.WHT_ROOK_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.KNIGHT_VAL:
                    self.whiteTotalPieceVal += P.WHT_KNIGHT_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.BISHOP_VAL:
                    self.whiteTotalPieceVal += P.WHT_BISHOP_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.QUEEN_VAL:
                    self.whiteTotalPieceVal += P.WHT_QUEEN_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.KING_VAL:
                    self.whiteTotalPieceVal += P.WHT_KING_POS_VAL_MID[loc[i][0]][loc[i][1]]
            elif pieces[i].color == P.BLACK:
                self.blackTotalPieceVal += pieces[i].value
                if pieces[i].value == P.PAWN_VAL:
                    self.blackTotalPieceVal += P.BLK_PAWN_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.ROOK_VAL:
                    self.blackTotalPieceVal += P.BLK_ROOK_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.KNIGHT_VAL:
                    self.blackTotalPieceVal += P.BLK_KNIGHT_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.BISHOP_VAL:
                    self.blackTotalPieceVal += P.BLK_BISHOP_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.QUEEN_VAL:
                    self.blackTotalPieceVal += P.BLK_QUEEN_POS_VAL[loc[i][0]][loc[i][1]]
                elif pieces[i].value == P.KING_VAL:
                    self.blackTotalPieceVal += P.BLK_KING_POS_VAL_MID[loc[i][0]][loc[i][1]]
    
    #def getAndRemoveLastState(self, num):
    #    rem = self.prevBoards[len(self.prevBoards) - num]
    #    for i in reversed(range(len(self.prevBoards) - 1, len(self.prevBoards) - num + 1)):
    #        self.prevBoards.pop(i)
    #    
    #    return rem
    #
    #def getAndRemoveLastState(self):
    #    return getAndRemoveLastState(self, 1)
    
    def wipe(self):
        for space in self.board:
            space = P.Empty()
    
    def getAllPieces(self, selectColor=None):
        pieces = []
        locations = []
        
        for x in range(0, 8):
            for y in range(0, 8):
                sel = self.board[x][y]
                if (isinstance(sel, P.Piece) and (selectColor == None or sel.color == selectColor)):
                    pieces.append(sel)
                    locations.append((x, y))
        
        return pieces, locations
    
    def getPiece(self, space):
        return self.board[space[0]][space[1]]

    def copy(self):
        cpyBoard = Board(True)
        cpyBoard.board = [row[:] for row in self.board]
        cpyBoard.unmoved = self.unmoved[:]
        cpyBoard.whiteChecked = self.whiteChecked
        cpyBoard.blackChecked = self.blackChecked
        cpyBoard.turn = self.turn
        cpyBoard.whiteKingId = self.whiteKingId
        cpyBoard.blackKingId = self.blackKingId
        cpyBoard.whiteTotalPieceVal = self.whiteTotalPieceVal
        cpyBoard.blackTotalPieceVal = self.blackTotalPieceVal
        cpyBoard.passentable = self.passentable

        return cpyBoard
    
    def pieceUnmoved(self, pieceIdent):
        return self.unmoved.count(pieceIdent)