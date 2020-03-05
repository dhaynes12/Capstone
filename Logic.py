from Board import Board
import Pieces as P
from copy import deepcopy

def select_piece(state, x, y):
    return state.board[x][y].validMoves(state, (x, y))
    
def move_piece(state, selX, selY, move):
    st = deepcopy(state)
    
    st.prevBoards.append(deepcopy(st.board))
    
    st.board[move.x()][move.y()] = deepcopy(st.board[selX][selY])
    st.board[selX][selY] = P.Empty()
    
    piece = st.board[move.x()][move.y()]
    
    if move.special == P.EN_PASSENT:
        adjust = -1
        if (st.board[move.x()][move.y()].color == P.BLACK):
            adjust = 1
        
        st.board[move.x()][move.y()+adjust] = P.Empty()   
    elif move.special == P.CASTLE:
        rookY = 0
        
        if(state.turn == P.BLACK):
            rookY = 7
        
        if (move.x() == 2):
            st.board[3][0] = deepcopy(st.board[0][0])
            st.board[0][0] = P.Empty()
            st.board[3][0].moved = True
        elif (move.x() == 6):
            st.board[5][0] = deepcopy(st.board[7][0])
            st.board[7][0] = P.Empty()
            st.board[5][0].moved = True
    elif (isinstance(st.board[move.x()][move.y()], P.Pawn) and ((piece.color == P.WHITE and move.y() == 7) or (piece.color == P.BLACK and move.y() == 0))):
        promotion = P.Queen(piece.ident, piece.color)
        st.board[move.x()][move.y()] = promotion
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
    
    st.whiteChecked = False
    st.blackChecked = False
    piece.moved = True
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

"""Returns True if the king of the specified color cannot make any moves"""
def is_checkmate(state, color):
    kingId = 0
    enemyColor = None
    if (color == P.WHITE):
        kingId = state.whiteKingId
        enemyColor = P.BLACK
    else:
        kingId = state.blackKingId
        enemyColor = P.WHITE
    
    king, kingSpace = P.searchForPiece(kingId, state)
    
    return king.validMoves(state, kingSpace) in P.getValidMoves(enemyColor, state)
   
   
def undo(state, movesBack):
    st = deepcopy(state)
    
    st.board = st.getAndRemoveLastState(movesBack)
    
    #Moving back by an odd number means we're moving to a state that was during another player's turn
    if movesBack % 2 == 1:
        st.turn = P.swapTurn(st.turn)
    
    set_check(st)
    
    return st
    