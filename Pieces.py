import Board

"""Color Constants"""
WHITE = 0
BLACK = 1

"""Special Move Constants"""
CASTLE = 0
EN_PASSENT = 1
NON_CAPTURE = 2

"""Piece Values"""
PAWN_VAL = 1
KNIGHT_VAL = 3
BISHOP_VAL = 3.5
ROOK_VAL = 7
QUEEN_VAL = 9
KING_VAL = 0

def swapTurn(color):
    if (color == WHITE):
        return BLACK
    
    return WHITE

"""Returns a space that's a number of horizontal and vertical moves away from the given space.

   space - A tuple of x and y coordinates which represents one of the spaces
   move - A tuple of number of horizontal movements and number of vertical movements from the given space"""
def moveSpace(space, move):
    return (space[0] + move[0], space[1] + move[1])

"""Returns the piece/empty occupying a space relative to the current space given. If the given movement goes off the board,
   None is returned.

   board - The 2d list that represents the current state of the game.
   space - A tuple of x and y coordinates which represents one of the spaces
   move - A tuple of number of horizontal movements and number of vertical movements from the given space"""
def isOccupiedBy(board, space, move):
    if board == None:
        return None
        
    look = moveSpace(space, move)
    
    if (look[0] > 7 or look[1] > 7 or look[0] < 0 or look[1] < 0):
        return None
    
    return board[look[0]][look[1]]

"""Returns the pieces/empties occupying a line of spaces that point in a direction specified by xIncrease and yIncrease.
   This line ends at the edge of the board, just before an allied piece, or directly on an opposing piece
   
   board - The 2d list that represents the current state of the game.
   space - A tuple of x and y coordinates which represents one of the spaces
   color - The color of the piece that's calling this function
   xIncrease - The x direction of the line
   yIncrease - The y direction of the line"""
def lookLine(board, space, color, xIncrease, yIncrease):
    v = []
    x = xIncrease
    y = yIncrease
    occupy = Empty()
    
    while isinstance(occupy, Empty):
        occupy = isOccupiedBy(board, space, (x, y))
        
        if isinstance(occupy, Empty) or (isinstance(occupy, Piece) and occupy.color != color):
            v.append(Move(moveSpace(space, (x, y)), originSpace=space))
            x += xIncrease
            y += yIncrease
    
    return v

"""Gets all valid moves from all pieces of the specified color

   color - The color of the pieces that will have their moves returned
   b - The Board object that represents the current state of the game.
   kingCheck - A boolean that indicates if this function is called as part of a castle check
   ignorePiece - Id of a piece you want to not get the valid moves of"""
def getValidMoves(color, b, kingCheck = None, ignorePiece=None):
    moves = []

    #print("\nGETVALIDMOVES OUTPUT")
    #print("--------------------")
    for x in range(0, 8):
        for y in range(0, 8):
            if (isinstance(b.board[x][y], Piece) and b.board[x][y].color == color and (ignorePiece == None or b.board[x][y].ident != ignorePiece)):
                #print("PIECE: ", b.board[x][y], ",", b.board[x][y].color, ",",  x, ",", y)
                moves.extend(b.board[x][y].validMoves(b, (x, y), True))
                #for m in b.board[x][y].validMoves(b, (x, y), True):
                #    print("\t", m)
    
    return moves

def hasSharedSpaces(list1, list2):
    for l in list1:
        if list2.count(l):
            return True
    
    return False

def spacesAreFree(b, spaces):
    for space in spaces:
        if not isinstance(b.board[space[0]][space[1]], Empty):
            return False
    
    return True

def colorToStr(color):
    if color == WHITE:
        return "white"
    elif color == BLACK:
        return "black"
    
    return "invalid"

def searchForPiece(pieceId, board):
    for x in range(0, 8):
        for y in range(0, 8):
            if (isinstance(board[x][y], Piece) and board[x][y].ident == pieceId):
                return board[x][y], (x, y)
    
    return None, None

class Move():
    def __init__(self, space, special=None, originSpace=None):
        self.space = space
        self.special = special
        self.originSpace = originSpace
    
    def x(self):
        return self.space[0]
    
    def y(self):
        return self.space[1]
    
    def originX(self):
        return self.originSpace[0]
        
    def originY(self):
        return self.originSpace[1]
    
    def compareOriginSpace(self, coords):
        return self.originSpace[0] == coords[0] and self.originSpace[1] == coords[1]
    
    def __eq__(self, compare):
        if (isinstance(compare, Move)):
            return self.space == compare.space and self.special == compare.special
        elif (isinstance(compare, tuple)):
            return self.space[0] == compare[0] and self.space[1] == compare[1]
        
        raise TypeError
        
    def __str__(self):
        return "Move: " + "(" + str(self.space[0]) + ", " + str(self.space[1]) + ")" + " -- Special: " + str(self.special)

"""Used to indicate empty spaces, because None is used to indicate that a given set of coordinates are off the board"""
class Empty():
    def __init__(self):
        pass
    
    def validMoves(self, b, space):
        return []

"""The class which all chess pieces inherit from"""
class Piece():
    def __init__(self, ident, color, moved, value, image):
        self.ident = ident
        self.color = color
        self.value = value
        self.image = image
        self.moved = moved
    
    """b - The Board object that represents the current state of the game and contains prior states.
       space - A tuple of x and y coordinates which represent the piece's current space
       kingCheck - A boolean that indicates if this function is called as part of a castle check"""
    def validMoves(self, b, space, kingCheck=None):
        return []

class Pawn(Piece):
    def __init__(self, ident, color, moved=False):
        Piece.__init__(self, ident, color, moved, PAWN_VAL, "pieces/" + colorToStr(color) + "_pawn.png")
        
        if (self.color == WHITE):
            self.upMove = 1
        else:
            self.upMove = -1
    
    def validPassent(self, pawnSpace, pawnId, pastBoard):
        upTwo = isOccupiedBy(pastBoard, pawnSpace, (0, self.upMove * 2))
        
        if (isinstance(upTwo, Pawn) and upTwo.ident == pawnId and not upTwo.moved):
            return True
        
        return False
    
    def validMoves(self, b, space, kingCheck=None):
        v = []
        
        """Standard Movement"""
        if (isinstance(isOccupiedBy(b.board, space, (0, self.upMove)), Empty)):
            v.append(Move(moveSpace(space, (0, self.upMove)), NON_CAPTURE, originSpace=space))
        
        """Double Move"""
        if (not self.moved and 
        isinstance(isOccupiedBy(b.board, space, (0, self.upMove)), Empty) and 
        isinstance(isOccupiedBy(b.board, space, (0, self.upMove * 2)), Empty)):            
            v.append(Move(moveSpace(space, (0, self.upMove * 2)), NON_CAPTURE, originSpace=space))
        
        """Capture"""
        upLeft = isOccupiedBy(b.board, space, (-1, self.upMove))
        upRight = isOccupiedBy(b.board, space, (1, self.upMove))
        if (isinstance(upLeft, Piece) and upLeft.color != self.color):
            v.append(Move(moveSpace(space, (-1, self.upMove)), originSpace=space))
        
        if (isinstance(upRight, Piece) and upRight.color != self.color):
            v.append(Move(moveSpace(space, (1, self.upMove)), originSpace=space))
        
        """En-Passent"""
        left = isOccupiedBy(b.board, space, (-1, 0))
        right = isOccupiedBy(b.board, space, (1, 0))
        if (isinstance(left, Pawn) and self.validPassent(moveSpace(space, (-1, 0)), left.ident, b.prevBoard)):
            v.append(Move(moveSpace(space, (-1, self.upMove)), EN_PASSENT, originSpace=space))
            
        if (isinstance(right, Pawn) and self.validPassent(moveSpace(space, (1, 0)), right.ident, b.prevBoard)):
            v.append(Move(moveSpace(space, (1, self.upMove)), EN_PASSENT, originSpace=space))
        
        return v

class Knight(Piece):
    def __init__(self, ident, color, moved=False):
        Piece.__init__(self, ident, color, moved, KNIGHT_VAL, "pieces/" + colorToStr(color) + "_knight.png")
    
    def validMoves(self, b, space, kingCheck=None):
        
        v = []
        posMoves = [
                    (1, 2),
                    (-1, 2),
                    (2, 1),
                    (2, -1),
                    (1, -2),
                    (-1, -2),
                    (-2, -1),
                    (-2, 1)
                   ]
        
        for i in posMoves:
            occupy = isOccupiedBy(b.board, space, i)
            
            if (isinstance(occupy, Empty) or (isinstance(occupy, Piece) and occupy.color != self.color)):
                v.append(Move(moveSpace(space, i), originSpace=space))
        
        return v

class Bishop(Piece):
    def __init__(self, ident, color, moved=False):
        Piece.__init__(self, ident, color, moved, BISHOP_VAL, "pieces/" + colorToStr(color) + "_bishop.png")
    
    def validMoves(self, b, space, kingCheck=None):
        
        v = []
        
        v.extend(lookLine(b.board, space, self.color, 1, 1))
        v.extend(lookLine(b.board, space, self.color, 1, -1))
        v.extend(lookLine(b.board, space, self.color, -1, -1))
        v.extend(lookLine(b.board, space, self.color, -1, 1))
        
        return v

class Rook(Piece):
    def __init__(self, ident, color, moved=False):
        Piece.__init__(self, ident, color, moved, ROOK_VAL, "pieces/" + colorToStr(color) + "_rook.png")
    
    def validMoves(self, b, space, kingCheck=None):
        
        v = []
        
        v.extend(lookLine(b.board, space, self.color, 0, 1))
        v.extend(lookLine(b.board, space, self.color, 1, 0))
        v.extend(lookLine(b.board, space, self.color, 0, -1))
        v.extend(lookLine(b.board, space, self.color, -1, 0))
        
        return v

class Queen(Piece):
    def __init__(self, ident, color, moved=False):
        Piece.__init__(self, ident, color, moved, QUEEN_VAL, "pieces/" + colorToStr(color) + "_queen.png")
    
    def validMoves(self, b, space, kingCheck=None):
        
        v = []
        
        v.extend(lookLine(b.board, space, self.color, 0, 1))
        v.extend(lookLine(b.board, space, self.color, 1, 0))
        v.extend(lookLine(b.board, space, self.color, 0, -1))
        v.extend(lookLine(b.board, space, self.color, -1, 0))
        v.extend(lookLine(b.board, space, self.color, 1, 1))
        v.extend(lookLine(b.board, space, self.color, 1, -1))
        v.extend(lookLine(b.board, space, self.color, -1, -1))
        v.extend(lookLine(b.board, space, self.color, -1, 1))
        
        return v

class King(Piece):
    def __init__(self, ident, color, moved=False):
        Piece.__init__(self, ident, color, moved, KING_VAL, "pieces/" + colorToStr(color) + "_king.png")
        
        if (self.color == WHITE):
            self.upMove = 1
        else:
            self.upMove = -1
    
    def validCastle(self, spaces):
        for space in spaces:
            if not isinstance(isOccupiedBy(b.board, space, (0, self.upMove)), Empty):
                return False
        
        
    
    def validMoves(self, b, space, kingCheck=None):
        v = []
        
        """Standard Movement. Doesn't take check into account -- game itself will revert
        a move if it puts the King in check"""
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 and y == 0):
                    continue
                occupy = isOccupiedBy(b.board, space, (x, y))
                if (isinstance(occupy, Empty) or (isinstance(occupy, Piece) and occupy.color != self.color)):
                    v.append(Move(moveSpace(space, (x, y)), originSpace=space))
        
        """Castling"""
        """Don't check for castling if this validMoves is called as part of another king's castle check"""
        if (not kingCheck):
            leftRookSpace = b.board[0][space[1]]
            rightRookSpace = b.board[7][space[1]]
            
            leftRookUnmoved = isinstance(leftRookSpace, Rook) and not leftRookSpace.moved
            rightRookUnmoved = isinstance(rightRookSpace, Rook) and not rightRookSpace.moved
            
            checked = (b.whiteChecked and self.color == WHITE) or (b.blackChecked and self.color == BLACK)
            
            if (not checked and not self.moved and (leftRookUnmoved or rightRookUnmoved)):
                opposer = WHITE
                if (self.color == WHITE):
                    opposer = BLACK
                
                dangerSpaces = []
                for move in getValidMoves(opposer, b, True):
                    if(move.special == None):
                        dangerSpaces.append(move.space)
                
                if (leftRookUnmoved):
                    leftSpaces = [moveSpace(space, (-1, 0)), moveSpace(space, (-2, 0)), moveSpace(space, (-3, 0))]
                    
                    if (not hasSharedSpaces(dangerSpaces, leftSpaces) and spacesAreFree(b, leftSpaces)):
                        v.append(Move(moveSpace(space, (-2, 0)), CASTLE, originSpace=space))
                
                if (rightRookUnmoved):
                    rightSpaces = [moveSpace(space, (1, 0)), moveSpace(space, (2, 0))]
                    
                    if (not hasSharedSpaces(dangerSpaces, rightSpaces) and spacesAreFree(b, rightSpaces)):
                        v.append(Move(moveSpace(space, (2, 0)), CASTLE, originSpace=space))
        
        return v