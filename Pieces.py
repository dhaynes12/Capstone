"""Color Constants"""
WHITE = 0
BLACK = 1

"""Special Move Constants"""
CASTLE = 0
EN_PASSENT = 1

"""Returns a space that's a number of horizontal and vertical moves away from the given space.

   space - A tuple of x and y coordinates which one of the spaces
   move - A tuple of number of horizontal movements and number of vertical movements from the given space"""
def moveSpace(space, move):
    return (space[0] + move[0], space[1] + move[1])

"""Returns the piece/empty occupying a space relative to the current space given. If the given movement goes off the board,
   None is returned.

   board - The 2d list that represents the current state of the game.
   space - A tuple of x and y coordinates which one of the spaces
   move - A tuple of number of horizontal movements and number of vertical movements from the given space"""
def isOccupiedBy(board, space, move):
    look = moveSpace(space, move)
    
    if (look(0) > 7 or look(1) > 7 or look(0) < 0 or look(1) < 0):
        return None
    
    return board[look(0)][look(1)]

def lookLine(board, space, color, xIncrease, yIncrease):
    v = []
    x = xIncrease
    y = yIncrease
    occupy = Empty()
    
    while isinstance(occupy, Empty):
        occupy = isOccupiedBy(board, space, (x, y))
        
        if isinstance(occupy, Empty) or occupy.color != color:
            v.append(Move(moveSpace(space, (x, y), None)))
    
    return v
            

class Move():
    def __init__(self, space, special):
        self.space = space
        self.special = special

"""Used to indicate empty spaces, because None is used to indicate that a given set of coordinates are off the board"""
class Empty():
    def __init__(self):
        pass

"""The class which all chess pieces inherit from"""
class Piece():
    def __init__(self, color, value, image):
        self.color = color
        self.value = value
        self.image = image
    
    """board - The 2d list that represents the current state of the game.
       space - A tuple of x and y coordinates which represent the piece's current space"""
    def validMoves(board, space):
        return []

class Pawn(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 1, "")
        
        if (self.color == WHITE):
            self.upMove = 1
        else:
            self.upMove = -1
    
    def validMoves(self, board, space):
        v = []
        
        if (isinstance(isOccupiedBy(board, space, (0, self.upMove)), Empty)):
            v.append(Move(moveSpace(space, (0, self.upMove)), None))
        
        if (isOccupiedBy(board, space, (1, self.upMove).color != self.color)):
            v.append(Move(moveSpace(space, (1, self.upMove)), None))
        
        if (isOccupiedBy(board, space, (-1, self.upMove).color != self.color)):
            v.append(Move(moveSpace(space, (-1, self.upMove)), None))
        
        #TODO: En-passent
        
        return v

class Knight(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 3, "")
    
    def validMoves(self, board, space):
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
            occupy = isOccupiedBy(board, space, i)
            
            if (isinstance(occupy, Empty) or occupy.color != self.color):
                v.append(moveSpace(space, moveSpace(space, Move(moveSpace(space, i), None))))
        
        return v

class Bishop(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 3.5, "")
    
    def validMoves(self, board, space):
        v = []
        
        v.extend(lookLine(board, space, self.color, 1, 1))
        v.extend(lookLine(board, space, self.color, 1, -1))
        v.extend(lookLine(board, space, self.color, -1, -1))
        v.extend(lookLine(board, space, self.color, -1, 1))
        
        return v

class Rook(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 7, "")
    
    def validMoves(self, board, space):
        v = []
        
        v.extend(lookLine(board, space, self.color, 0, 1))
        v.extend(lookLine(board, space, self.color, 1, 0))
        v.extend(lookLine(board, space, self.color, 0, -1))
        v.extend(lookLine(board, space, self.color, -1, 0))
        
        return v

class Queen(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 9, "")
    
    def validMoves(self, board, space):
        v = []
        
        v.extend(lookLine(board, space, self.color, 0, 1))
        v.extend(lookLine(board, space, self.color, 1, 0))
        v.extend(lookLine(board, space, self.color, 0, -1))
        v.extend(lookLine(board, space, self.color, -1, 0))
        v.extend(lookLine(board, space, self.color, 1, 1))
        v.extend(lookLine(board, space, self.color, 1, -1))
        v.extend(lookLine(board, space, self.color, -1, -1))
        v.extend(lookLine(board, space, self.color, -1, 1))
        
        return v

class King(Piece):
    def __init__(self, color):
        Piece.__init__(self, color, 0, "")
    
    def validMoves(self, board, space):
        v = []
        
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x == 0 and y == 0):
                    continue
                occupy = isOccupiedBy(board, space, (x, y))
                if (isinstance(occupy, Empty) or occupy.color != self.color):
                    v.append(Move(moveSpace(space, (x, y)), None))
        
        #TODO: Restricting King from being put in danger
        #TODO: Castling. Look at rules of castling, complex.