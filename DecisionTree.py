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
        self.nextMoves = []         # list of next possible moves
        self.weight = 0             # How good of a move is current node
        self.space = space          # The coordinates of the piece being moved
        self.move = move            # The coordinates that the piece is being moved to

        # if depth is at limit call weight function
        if depth == depthLim:
            self.setWeight()
        else:       # else generate list of next possible moves
            global maxNodeDepth
            if (depth > maxNodeDepth):
                maxNodeDepth = depth


    def genNextMoves(self):
        
        pieces, locs = self.state.getAllPieces(self.state.turn)
        for i in range(0, len(pieces)):
            if not isinstance(pieces[i], P.Piece):
                continue
            else:
                for move in pieces[i].validMoves(self.state, locs[i]):
                    tempState = Logic.move_piece(self.state, locs[i][0], locs[i][1], move)
                    if (tempState != None):
                        tempNode = Node(self.color, tempState, self.depth+1, self.depthLim, self.heuristic, locs[i], move)
                        self.nextMoves.append(tempNode)
        
        random.shuffle(self.nextMoves)
        

    # Generate how good a move is if node is a leaf node
    def setWeight(self):
    
        if (self.heuristic == BASIC):
            """AI's total piece value compared to opponent's total piece value"""
            self.weight = (self.state.whiteTotalPieceVal - self.state.blackTotalPieceVal) * 10
            if (self.color == P.BLACK):
                self.weight *= -1
            
            """Number of moves that AI has compared to number of moves opponent has"""
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
    
    print("Turn:", state.turn)
    print("Calculation Time:", endTime - startTime, "seconds")
    print("Max Node Depth:", maxNodeDepth)
    print("Total Nodes:", totalNodes)
    print()
    
    maxNodeDepth = 0
    totalNodes = 0
    
    return node

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
            for n in node.nextMoves:
                tempVal, jnkState = ABPruning(n, node.alpha, node.beta)
                if tempVal < node.beta:
                    node.beta = tempVal
                    nextMove = n
                if node.beta <= node.alpha:
                    break
            return node.beta, nextMove
        else:
            for n in node.nextMoves:
                tempVal, jnkState = ABPruning(n, node.alpha, node.beta)
                if tempVal > node.alpha:
                    node.alpha = tempVal
                    nextMove = n
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