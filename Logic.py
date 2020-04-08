from Board import Board, EMPTY
import Pieces as P
from copy import deepcopy

def select_piece(state, x, y):
    return state.board[x][y].validMoves(state, (x, y))
    
def move_piece(state, selX, selY, move):
    st = state.copy()
    
    """Update total piece value if there's a capture"""
    if (isinstance(st.board[move.x()][move.y()], P.Piece)):
        if st.board[move.x()][move.y()].color == P.WHITE:
            st.whiteTotalPieceVal -= st.board[move.x()][move.y()].value
        elif st.board[move.x()][move.y()].color == P.BLACK:
            st.blackTotalPieceVal -= st.board[move.x()][move.y()].value
    
    st.board[move.x()][move.y()] = st.board[selX][selY]
    st.board[selX][selY] = EMPTY
    
    piece = st.board[move.x()][move.y()] 
    
    if move.special == P.EN_PASSENT:
        adjust = -1
        if (st.board[move.x()][move.y()].color == P.BLACK):
            adjust = 1
        
        if st.board[move.x()][move.y()+adjust].color == P.WHITE:
            st.whiteTotalPieceVal -= 1
        elif st.board[move.x()][move.y()+adjust].color == P.BLACK:
            st.blackTotalPieceVal -= 1
        st.board[move.x()][move.y()+adjust] = EMPTY
    elif move.special == P.CASTLE:
        if (move.x() == 2):
            st.board[3][move.y()] = st.board[0][move.y()]
            st.board[0][move.y()] = EMPTY
            st.unmoved.remove(st.board[3][move.y()].ident)
        elif (move.x() == 6):
            st.board[5][move.y()] = st.board[7][move.y()]
            st.board[7][move.y()] = EMPTY
            st.unmoved.remove(st.board[5][move.y()].ident)
    elif (isinstance(st.board[move.x()][move.y()], P.Pawn) and ((piece.color == P.WHITE and move.y() == 7) or (piece.color == P.BLACK and move.y() == 0))):
        promotion = P.Queen(piece.ident, piece.color)
        st.board[move.x()][move.y()] = promotion
        if (piece.color == P.WHITE):
            st.whiteTotalPieceVal += (P.QUEEN_VAL - P.PAWN_VAL)
        elif (piece.color == P.BLACK):
            st.blackTotalPieceVal += (P.QUEEN_VAL - P.PAWN_VAL)
        """Need to figure out how to let the user select the promotion"""
    
    kingId = 0
    enemyKingId = 0
    if (st.turn == P.WHITE):
        kingId = st.whiteKingId
        enemyKingId = st.blackKingId
    else:
        kingId = st.blackKingId
        enemyKingId = st.whiteKingId
    
    """Check if the moving player's King wasn't put in danger. Throw out the board if he is in danger, and indicate this by returning None"""
    king, kingSpace = P.searchForPiece(kingId, st.board)
    if ((st.turn == P.WHITE and kingSpace in P.getValidMoves(P.BLACK, st)) or (st.turn == P.BLACK and kingSpace in P.getValidMoves(P.WHITE, st))):
        return None
    
    if (st.passentable != None):
        st.passentable = None
    
    """Determining if the pawn that just moved can suffer from en-passenting"""
    if (isinstance(piece, P.Pawn) and (st.pieceUnmoved(piece.ident) and abs(selY - move.y()) == 2)):
        st.passentable = move.space
    
    st.whiteChecked = False
    st.blackChecked = False
    if (st.pieceUnmoved(piece.ident)):
        st.unmoved.remove(piece.ident)
    set_check(st)
    
    st.turn = P.swapTurn(st.turn)
        
    return st

"""Check if the opposing king is put in check, and sets the corresponding check boolean if they are in check"""
def set_check(state):
    enemyKingId = 0
    
    if (state.turn == P.WHITE):
        enemyKingId = state.blackKingId
    elif (state.turn == P.BLACK):
        enemyKingId = state.whiteKingId
    
    enemyKing, enemyKingSpace = P.searchForPiece(enemyKingId, state.board)
    if (state.turn == P.WHITE and enemyKingSpace in P.getValidMoves(P.WHITE, state)):
        state.blackChecked = True
    elif (state.turn == P.BLACK and enemyKingSpace in P.getValidMoves(P.BLACK, state)):
        state.whiteChecked = True

"""Returns True if the king of the specified color cannot get itself out of danger. Returns None if the specified
side cannot make any moves"""
def is_checkmate(state, color):
    kingId = 0
    enemyColor = None
    if (color == P.WHITE):
        kingId = state.whiteKingId
        enemyColor = P.BLACK
    else:
        kingId = state.blackKingId
        enemyColor = P.WHITE
    
    king, kingSpace = P.searchForPiece(kingId, state.board)
    
    kingCantMove = True
    checkmate = True
    opponentMoves = P.getValidMoves(enemyColor, state)
    friendMoves = P.getValidMoves(color, state, ignorePiece = king.ident)
    
    for kingMove in king.validMoves(state, kingSpace):
        if (kingMove not in opponentMoves):
            pieceAtSpace = state.getPiece(kingMove.space)
            if isinstance(pieceAtSpace, P.Empty):
                if move_piece(state, kingSpace[0], kingSpace[1], kingMove) == None:
                    continue
                kingCantMove = False
            
            if isinstance(pieceAtSpace, P.Piece) and (move_piece(state, kingSpace[0], kingSpace[1], kingMove) == None):
                noProtect = False
                if (kingMove in friendMoves):
                    for move in friendMoves:
                        if (move == kingMove.space and move_piece(state, move.originX(), move.originY(), move) == None):
                            noProtect = True
                            break
                else:
                    noProtect = True
                    
                if (noProtect):
                    continue
                    
            kingCantMove = False
            checkmate = False
            break
    
    if checkmate:
        oppPieces, oppSpaces = piecesEndangeringSpace(state, opponentMoves, kingSpace)
        
        """As far as I know, it's possible for only one piece to directly endanger the King at a given time"""
        if (len(oppPieces) > 1):
            raise Exception("Somehow multiple pieces directly endangered the King, which would only happen if the King finished its turn still in check")
        
        if (len(oppPieces) == 0):
            checkmate = False
        elif (type(oppPieces[0]) == P.Queen or type(oppPieces[0]) == P.Rook or type(oppPieces[0]) == P.Bishop):
            for between in betweenSpaces(state, kingSpace, oppSpaces[0]):
                    if between in friendMoves:
                        move = friendMoves[friendMoves.index(between)]
                        if move_piece(state, move.originX(), move.originY(), move) != None:
                            checkmate = False
                            break
    
    if not checkmate and kingCantMove and len(friendMoves) == 0:
        return None
        
    return checkmate
    
   
def undo(state, movesBack):
    st = state.copy()
    
    st.board = st.getAndRemoveLastState(movesBack)
    
    #Moving back by an odd number means we're moving to a state that was during another player's turn
    if movesBack % 2 == 1:
        st.turn = P.swapTurn(st.turn)
    
    set_check(st)
    
    return st


def getPiecesMovesFromList(movesList, pieceSpace):
	pieceMoves = []
	for move in movesList:
		if move.compareOriginSpace(pieceSpace):
			pieceMoves.append(deepcopy(move))
	
	return pieceMoves
	

def piecesEndangeringSpace(state, movesList, space):
    pieces = []
    pieceSpaces = []
    for move in movesList:
        if (move.originSpace not in pieceSpaces) and (space in state.getPiece(move.originSpace).validMoves(state, move.originSpace)):
            pieces.append(state.getPiece(move.originSpace))
            pieceSpaces.append(move.originSpace)
    
    return pieces, pieceSpaces

"""Returns the spaces between two spaces. space1 and space2 must be aligned so that they are perfectly horizontal, vertical, or diagonal"""
def betweenSpaces(state, space1, space2):
    spaces = []
    minX = min(space1[0], space2[0])
    maxX = max(space1[0], space2[0])
    minY = min(space1[1], space2[1])
    maxY = max(space1[1], space2[1])
    
    """Diagonal Look"""
    if space1[0] != space2[0] and space1[1] != space2[1]:
    
        leftmostSpace = None
        rightmostSpace = None
        if (space1[0] == maxX):
            leftmostSpace = space2
            rightmostSpace = space1
        else:
            leftmostSpace = space1
            rightmostSpace = space2
        loops = 0
        loopChange = 0
        if (leftmostSpace[1] > rightmostSpace[1]):
            loops = -1
            loopChange = -1
        else:
            loops = 1
            loopChange = 1
            
        for x in range(leftmostSpace[0]+1, rightmostSpace[0]):
            spaces.append((x, leftmostSpace[1]+loops))
            loops += loopChange
    elif space1[0] == space2[0] and space1[1] != space2[1]:
        for y in range(minY+1, maxY):
            spaces.append((minX, y))
    elif space1[0] != space2[0] and space1[1] == space2[1]:
        for x in range(minX+1, maxX):
            spaces.append((x, minY))
    
    return spaces