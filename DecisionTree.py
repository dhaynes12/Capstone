from Board import Board
import Pieces as P
import Logic
from copy import deepcopy
import time
import math
import random

"""Global Values"""
maxNodeDepth = 0
totalNodes = 0
prevMove = None

"""Heuristic Types"""
BASIC = 0
HASH = 1
BASIC_SORT = 2
NEGMAX = 3
HASH_SORT = 4
NEGMAX_POS = 5
BASIC_SORT_POS = 6
HASH_SORT_POS = 7

class AI_Exception(Exception):
    def __init__(self, state, mess, aiColor):
        self.state = state
        self.mess = mess
        self.aiColor = aiColor
    
    def __str__(self):
        return self.mess + "\nAI: " + P.colorToStr(self.aiColor) + "\nTurn during state: " + P.colorToStr(self.state.turn)

class Node(object):
    
    def __init__(self, color, state, depth, depthLim, heuristic, space = (0,0), move = P.Move((-1, -1))):
        global totalNodes
        totalNodes += 1
    
        self.state = state          # board state of the node
        self.color = color          # whether the AI controls the white or black pieces.
        self.depth = depth          # current depth of node
        self.depthLim = depthLim    # depth of how far the tree can evaluate
        self.heuristic = heuristic
        self.alpha = 0              # alpha and beta are values for pruning the tree
        self.beta = 0
        if (self.heuristic == HASH or self.heuristic == HASH_SORT or self.heuristic == HASH_SORT_POS):
            self.nextMoves = {}
        else:
            self.nextMoves = []
        self.weight = 0             # How good of a move is current node
        self.space = space          # The coordinates of the piece being moved
        self.move = move            # The coordinates that the piece is being moved to
        self._equalWeights = True

        if depth == depthLim or self.heuristic == BASIC_SORT or self.heuristic == HASH_SORT  or self.heuristic == BASIC_SORT_POS or self.heuristic == HASH_SORT_POS:
            self.setWeight()
        if depth < depthLim:
            global maxNodeDepth
            if (depth > maxNodeDepth):
                maxNodeDepth = depth


    def genNextMoves(self):
        
        pieces, locs = self.state.getAllPieces(self.state.turn)
        
        rangePieces = range(0, len(pieces))
        
        n = 0
        self._equalWeights = True
        
        if not (self.heuristic == BASIC_SORT or self.heuristic == HASH_SORT or self.heuristic == BASIC_SORT_POS or self.heuristic == HASH_SORT_POS):
            self._equalWeights = False
        
        locOfPieceWithPrevMove = None
        for i in rangePieces:
            if not isinstance(pieces[i], P.Piece):
                continue
            else:
                moves = pieces[i].validMoves(self.state, locs[i])
                rangeMoves = range(0, len(moves))
                
                for j in rangeMoves:
                    #if prevMove == None or (moves[j] != prevMove and moves[j].ident == prevMove.ident):
                    self.addNextMove(moves[j], locs[i])
                    #else:
                    #    locOfPieceWithPrevMove = locs[i]
                        
        #if (len(self.nextMoves) == 0 and prevMove != None):
        #    self.addNextMove(prevMove, locOfPieceWithPrevMove)
        
        if (self.heuristic == HASH):
            m = 0
            newDict = {}
            randomRange = list(range(0, len(self.nextMoves)))
            random.shuffle(randomRange)
            for r in randomRange:
                newDict[m] = self.nextMoves[r]
                m += 1
            self.nextMoves = newDict
        elif (self.heuristic == BASIC_SORT or self.heuristic == BASIC_SORT_POS):
            if not self._equalWeights:
                self.nextMoves = sorted(self.nextMoves, key=lambda x: x.weight, reverse=self.depth % 2 == 0)
            else:
                random.shuffle(self.nextMoves)
        elif (self.heuristic == HASH_SORT or self.heuristic == HASH_SORT_POS):
            self.nextMoves = dict(sorted(self.nextMoves.items(), key=lambda x: x[1].weight, reverse=True))
            
            for i in range(0, len(self.nextMoves)):
                print(self.nextMoves[i].weight)
        else:
            random.shuffle(self.nextMoves)
            

    def addNextMove(self, m, loc):
        tempState = Logic.move_piece(self.state, loc[0], loc[1], m)
        if (tempState != None):
            tempNode = Node(self.color, tempState, self.depth+1, self.depthLim, self.heuristic, loc, m)
            
            if self._equalWeights and len(self.nextMoves) > 0 and tempNode.weight != self.nextMoves[0].weight:
                self._equalWeights = False
            
            if (type(self.nextMoves) == dict):
                self.nextMoves[n] = tempNode
                n += 1
            else:
                self.nextMoves.append(tempNode)

    # Generate how good a move is if node is a leaf node
    def setWeight(self):
    
        if (self.heuristic >= BASIC and self.heuristic <= HASH_SORT):
            """AI's total piece value compared to opponent's total piece value"""
            self.weight = (self.state.whiteTotalPieceVal - self.state.blackTotalPieceVal) * 100
            if (self.color == P.BLACK):
                self.weight *= -1
            
            """Number of moves that AI"""
            if (self.state.turn == self.color):
                self.weight += len(self.nextMoves)
            else:
                self.weight -= len(self.nextMoves)
        elif (self.heuristic >= NEGMAX_POS and self.heuristic <= HASH_SORT_POS):
            self.weight = (self.state.whitePosPieceVal - self.state.blackPosPieceVal) * 1000
            if (self.color == P.BLACK):
                self.weight *= -1
            
            if (self.state.turn == self.color):
                self.weight += (len(self.nextMoves))
            else:
                self.weight -= len(self.nextMoves)
            
            #if ((self.color == P.WHITE and self.state.blackChecked) or (self.color == P.BLACK and self.state.whiteChecked)):
            #    self.weight += 1000
            #elif ((self.color == P.WHITE and self.state.whiteChecked) or (self.color == P.BLACK and self.state.blackChecked)):
            #    self.weight -= 1000
            
            #print(self.move, " -- Piece: ", self.space, " -- Weight: ", self.weight)

    # A quick and dirty copy function
    def copy(self):
        newNode = Node(self.color, self.state.copy(), self.depth, self.depthLim, self.heuristic, self.space, self.move)
        newNode.alpha = self.alpha
        newNode.beta = self.beta            
        newNode.nextMoves = self.nextMoves[:] 
        newNode.weight = self.weight
        return newNode


def aiSearch(state, depthLim, heuristic):
    global maxNodeDepth
    global totalNodes
    global prevMove
    
    startTime = time.perf_counter()
    
    tempNode = Node(state.turn, state, 0, depthLim, heuristic) 
    bestMoveLst = [tempNode]
    
    # Change herusitic value to 3 later
    if heuristic == NEGMAX or heuristic == NEGMAX_POS:
        for i in range(1, depthLim + 1):
            tempNode.depthLim = i
            value, node = ABNegPruning(tempNode, -math.inf, math.inf, bestMoveLst)
            bestMoveLst.append(node.state)
            #print("Current best move:", node.state, "\nCurrent best score:", value, "\nTotal Nodes:", totalNodes)
    else:
        value, node = ABPruning(tempNode, -math.inf, math.inf)
        print(value)
    
    endTime = time.perf_counter()
    
    print("Turn:", P.colorToStr(state.turn))
    print("Calculation Time:", endTime - startTime, "seconds")
    print("Max Node Depth:", maxNodeDepth)
    print("Total Nodes:", totalNodes)
    print()
    
    maxNodeDepth = 0
    totalNodes = 0
    
    if (isinstance(node, Node)):
        prevMove = node.move
    
    return node, endTime - startTime


def ABPruning (node, alpha, beta, nullMV = True):
    node.alpha = alpha
    node.beta = beta
    nextMove = None
    
    if node.depth == node.depthLim:
        return node.weight, nextMove
    node.genNextMoves()
    if len(node.nextMoves) == 0:
        return endStateCheck(node, nextMove)
    elif node.depth % 2 == 1:
        for n in node.nextMoves:
            tempVal, jnkState = ABPruning(n, node.alpha, node.beta)
            if tempVal < node.beta:
                node.beta = tempVal
                nextMove = n
            if node.beta <= node.alpha:
                break
        return node.beta, nextMove
    else:
        node.genNextMoves()
        if len(node.nextMoves) == 0:
            return endStateCheck(node, nextMove)
        elif node.depth % 2 == 1:
            for i in range(0, len(node.nextMoves)):
                tempVal, jnkState = ABPruning(node.nextMoves[i], node.alpha, node.beta)
                if tempVal < node.beta:
                    node.beta = tempVal
                    nextMove = node.nextMoves[i]
                if node.beta <= node.alpha:
                    break
            return node.beta, nextMove
        else:
            for i in range(0, len(node.nextMoves)):
                tempVal, jnkState = ABPruning(node.nextMoves[i], node.alpha, node.beta)
                if tempVal > node.alpha:
                    node.alpha = tempVal
                    nextMove = node.nextMoves[i]
                if node.beta <= node.alpha:
                    break
            return node.alpha, nextMove
 
def endStateCheck(node, nextMove):
    whiteCheckmate = Logic.is_checkmate(node.state, P.WHITE)
    blackCheckmate = Logic.is_checkmate(node.state, P.BLACK)
    if (whiteCheckmate or blackCheckmate):
        node.setWeight()
        if ((whiteCheckmate and node.color == P.BLACK) or (blackCheckmate and node.color == P.WHITE)):
            return (100000 * (node.depthLim+1)) / (node.depth + 1), nextMove
        return (-100000 * (node.depthLim+1)) / (node.depth + 1), nextMove
    elif (whiteCheckmate == None or blackCheckmate == None):
        return 0, nextMove
    raise AI_Exception(node.state, "Node has no next moves despite not being in an ending state", node.color)

# Checking for zugzwang (AT least one piece with a value greater than a pawn)
def checkZugzwang (node):
    pieces, loc = node.state.getAllPieces()
    for piece in pieces:
        if (node.state.turn == P.WHITE and piece.value >= P.PAWN_VAL and piece.color == P.WHITE) or (
            node.state.turn == P.BLACK and piece.value >= P.PAWN_VAL and piece.color == P.BLACK):
                return False
    return True

# nullMV is a variable to prevent nullmoves from chaining
def ABNegPruning (node, alpha, beta, bestMoveLst, nullMV = True):
    node.alpha = alpha
    node.beta = beta
    nextMove = None


    if node.depth == node.depthLim:
        return node.weight, nextMove
    # Checking in null move is possible (No check, can't chain, needs not to be the 0 move, no zugzwang)
    
    elif (nullMV and node.depth < node.depthLim - 2 and node.depth != 0 and checkZugzwang(node) is False):
        if (node.state.turn == P.WHITE and node.state.whiteChecked is False) or (
            node.state.turn == P.BLACK and node.state.blackChecked is False):
               
            # Copying the node and make a null move plus lower the depthLimit by R (2)
            copyNode = node.copy()
            copyNode.depthLim = node.depthLim - 2
            copyNode.state.turn = P.swapTurn(copyNode.state.turn)
            copyNode.depth += 1
            tempVal = 0
            if (beta == math.inf):
                tempVal, jnkState = ABNegPruning(node, -(1000001), -(1000000), bestMoveLst, False)
            else:
                tempVal, jnkState = ABNegPruning(node, -(beta), -(beta+1), bestMoveLst,  False)
            #print (tempVal, "beta:", beta)
            # if someNum is >= beta the return beta
            # need to figure out if I need to negate the tempVal
            if tempVal >= beta:
                #print("I just Null Pruned! on beta")
                return beta, nextMove 
    
    node.genNextMoves()
    if len(node.nextMoves) == 0:
        return endStateCheck(node, nextMove)
    else:
        for n in node.nextMoves:
            score, jnkState = ABNegPruning(n, -node.beta, -node.alpha, bestMoveLst, nullMV)
            if score > node.alpha:
                if score >= node.beta:
                    break
                node.alpha = score
                nextMove = n
        return node.alpha, nextMove

