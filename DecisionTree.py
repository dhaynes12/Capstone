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

"""Heuristic Types"""
BASIC = 0
HASH = 1
BASIC_SORT = 2
HASH_SORT = 4

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
        if (self.heuristic == HASH or self.heuristic == HASH_SORT):
            self.nextMoves = {}
        else:
            self.nextMoves = []
        self.weight = 0             # How good of a move is current node
        self.space = space          # The coordinates of the piece being moved
        self.move = move            # The coordinates that the piece is being moved to

        # if depth is at limit call weight function
        if depth == depthLim or self.heuristic == BASIC_SORT or self.heuristic == HASH_SORT:
            self.setWeight()
        if depth < depthLim:
            global maxNodeDepth
            if (depth > maxNodeDepth):
                maxNodeDepth = depth


    def genNextMoves(self):
        
        pieces, locs = self.state.getAllPieces(self.state.turn)
        
        rangePieces = range(0, len(pieces))
        
        n = 0
        equalWeights = True
        
        if not (self.heuristic == BASIC_SORT or self.heuristic == HASH_SORT):
            equalWeights = False
        
        for i in rangePieces:
            if not isinstance(pieces[i], P.Piece):
                continue
            else:
                moves = pieces[i].validMoves(self.state, locs[i])
                rangeMoves = range(0, len(moves))
                
                for j in rangeMoves:
                    tempState = Logic.move_piece(self.state, locs[i][0], locs[i][1], moves[j])
                    if (tempState != None):
                        tempNode = Node(self.color, tempState, self.depth+1, self.depthLim, self.heuristic, locs[i], moves[j])
                        
                        if equalWeights and len(self.nextMoves) > 0 and tempNode.weight != self.nextMoves[0].weight:
                            equalWeights = False
                        
                        if (type(self.nextMoves) == dict):
                            self.nextMoves[n] = tempNode
                            n += 1
                        else:
                            self.nextMoves.append(tempNode)
        
        if (self.heuristic == HASH):
            m = 0
            newDict = {}
            randomRange = list(range(0, len(self.nextMoves)))
            random.shuffle(randomRange)
            for r in randomRange:
                newDict[m] = self.nextMoves[r]
                m += 1
            self.nextMoves = newDict
        elif (self.heuristic == BASIC_SORT):
            if not equalWeights:
                self.nextMoves = sorted(self.nextMoves, key=lambda x: x.weight, reverse=self.depth % 2 == 0)
            else:
                random.shuffle(self.nextMoves)
        elif (self.heuristic == HASH_SORT):
            self.nextMoves = dict(sorted(self.nextMoves.items(), key=lambda x: x[1].weight, reverse=True))
            
            for i in range(0, len(self.nextMoves)):
                print(self.nextMoves[i].weight)
        else:
            random.shuffle(self.nextMoves)
        

    # Generate how good a move is if node is a leaf node
    def setWeight(self):
    
        """AI's total piece value compared to opponent's total piece value"""
        self.weight = (self.state.whiteTotalPieceVal - self.state.blackTotalPieceVal) * 10
        if (self.color == P.BLACK):
            self.weight *= -1
        
        """Number of moves that AI"""
        if (self.state.turn == self.color):
            self.weight += len(self.nextMoves)
        else:
            self.weight -= len(self.nextMoves)
        
        #if ((self.color == P.WHITE and self.state.blackChecked) or (self.color == P.BLACK and self.state.whiteChecked)):
        #    self.weight += 1000
        #elif ((self.color == P.WHITE and self.state.whiteChecked) or (self.color == P.BLACK and self.state.blackChecked)):
        #    self.weight -= 1000
        
        #print(self.move, " -- Piece: ", self.space, " -- Weight: ", self.weight)

def aiSearch(state, depthLim, heuristic):
    global maxNodeDepth
    global totalNodes
    
    startTime = time.perf_counter()
    
    tempNode = Node(state.turn, state, 0, depthLim, heuristic)   
    value, node = ABPruning(tempNode, -math.inf, math.inf)
    
    endTime = time.perf_counter()
    
    print("Turn:", P.colorToStr(state.turn))
    print("Calculation Time:", endTime - startTime, "seconds")
    print("Max Node Depth:", maxNodeDepth)
    print("Total Nodes:", totalNodes)
    print()
    
    maxNodeDepth = 0
    totalNodes = 0
    
    return node, endTime - startTime

def ABPruning (node, alpha, beta):
    node.alpha = alpha
    node.beta = beta
    nextMove = None
    
    if node.depth == node.depthLim:
        return node.weight, nextMove
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