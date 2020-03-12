from Board import Board
import Pieces as P
import Logic
from copy import deepcopy

class Node(object):
    
    def __init__(self, color, state, depth, depthLim, move = Move((-1, -1))):
        self.state = state          # board state of the node
        self.color = color          # whether the AI controls the white or black pieces.
        self.depth = depth          # current depth of node
        self.depthLim = depthLim    # depth of how far the tree can evaluate
        self.alpha = 0              # alpha and beta are values for pruning the tree
        self.beta = 0            
        self.nextMoves = []         # list of next possible moves
        self.weight = 0             # How good of a move is current node
        self.move = move

        # if depth is at limit call weight function
        if depth == depthLim:
            self.setWeight()
        else:       # else generate list of next possible moves
            self.genNextMoves()


    def genNextMoves(self):
        for piece, loc in state.getAllPieces(state.turn):
            if not isinstance(piece, Piece):
                continue
            else:
                # need to add optional state pass to board
                for move in piece.validMoves(self.state, loc):
                    tempState = deepcopy(self.state)
                    move_piece(tempState, loc[0], loc[1], move)
                    tempNode = Node(tempState, self.depth+1, self.depthLim, i)
                    self.nextMoves.append(tempNode)

    # Generate how good a move is if node is a leaf node
    def setWeight(self):
        self.weight = self.state.whiteTotalPieceVal - self.state.blackTotalPieceVal
        if (self.color == P.BLACK):
            self.weight *= -1

def ABPruning (node, alpha, beta):
    node.alpha = alpha
    node.beta = beta
    nextMove = None
    if node.depth == node.depthLim:
        return node.weight, nextMove
    elif len(node.nextMoves) == 0:
        if (board.checkEndState(node.state)):
            node.setWeight()
            if (node.weight > 0):
                return (1000 * node.depthLim+1) / node.depth+1, nextMove
            return (-1000 * node.depthLim+1) / node.depth+1, nextMove
        raise Exception("Node has no next moves despite not being in an ending state")
    elif node.depth % 2 == 1:
        for i in node.nextMoves:
            tempVal, jnkState = ABPruning(i, node.alpha, node.beta)
            if tempVal < node.beta:
                node.beta = tempVal
                nextMove = i
            if node.beta <= node.alpha:
                break
        return node.beta, nextMove
    else:
        for i in node.nextMoves:
            tempVal, jnkState = ABPruning(i, node.alpha, node.beta)
            if tempVal > node.alpha:
                node.alpha = tempVal
                nextMove = i
            if node.beta <= node.alpha:
                break
        return node.alpha, nextMove