import Pieces as P

class Board():

    def __init__(self, blank=False):
        self.board = []             # The game's current state, represented as a 2d array of Piece and Empty objects
        self.whiteChecked = False   # True when white's king is in check
        self.blackChecked = False   # True when black's king is in check
        self.turn = P.WHITE
        self.whiteKingId = 4
        self.blackKingId = 12
        self.whiteTotalPieceVal = 0
        self.blackTotalPieceVal = 0
        self.passentable = None
        
        for x in range(0, 8):
            self.board.append([])
            for y in range(0, 8):
                self.board[x].append(P.Empty())
        
        if (not blank):
            self.board[0][0] = P.Rook(0, P.WHITE)
            self.board[1][0] = P.Knight(1, P.WHITE)
            self.board[2][0] = P.Bishop(2, P.WHITE)
            self.board[3][0] = P.Queen(3, P.WHITE)
            self.board[4][0] = P.King(4, P.WHITE)
            self.board[7][0] = P.Rook(5, P.WHITE)
            self.board[6][0] = P.Knight(6, P.WHITE)
            self.board[5][0] = P.Bishop(7, P.WHITE)
            
            self.board[0][7] = P.Rook(8, P.BLACK)
            self.board[1][7] = P.Knight(9, P.BLACK)
            self.board[2][7] = P.Bishop(10, P.BLACK)
            self.board[3][7] = P.Queen(11, P.BLACK)
            self.board[4][7] = P.King(12, P.BLACK)
            self.board[7][7] = P.Rook(13, P.BLACK)
            self.board[6][7] = P.Knight(14, P.BLACK)
            self.board[5][7] = P.Bishop(15, P.BLACK)
            
            for i in range(0, 8):
                self.board[i][1] = P.Pawn(16 + i, P.WHITE)
                self.board[i][6] = P.Pawn(36 + i, P.BLACK)
        
        pieces, loc = self.getAllPieces()
        for piece in pieces:
            if piece.color == P.WHITE:
                self.whiteTotalPieceVal += piece.value
            elif piece.color == P.BLACK:
                self.blackTotalPieceVal += piece.value
    
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
        cpyBoard.whiteChecked = self.whiteChecked
        cpyBoard.blackChecked = self.blackChecked
        cpyBoard.turn = self.turn
        cpyBoard.whiteKingId = self.whiteKingId
        cpyBoard.blackKingId = self.blackKingId
        cpyBoard.whiteTotalPieceVal = self.whiteTotalPieceVal
        cpyBoard.blackTotalPieceVal = self.blackTotalPieceVal
        cpyBoard.passentable = self.passentable

        return cpyBoard