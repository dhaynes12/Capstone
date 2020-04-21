# Created by Devan and David
# For use in Chess AI Program

# Will contain the main portion of the GUI

import pygame
import time
import random # probably dont need
from InputBox import *
import os
import Logic
import Pieces as P
from Board import Board
from DecisionTree import ABPruning, Node, aiSearch, AI_Exception
from copy import deepcopy
import statistics
 
pygame.init() # Wont need later because main should have

# Variables for Gameplay
selectMoves = []
selectedSpace = None
state = Board()

# Display dimention -- Will need to change to match screen
display_width = 800
display_height = 600

# Some basic colors
black = (0,0,0)
darkGrey = (55,55,55)
lightGrey = (235,235,235)
skyBlue = (100,248,255)
darkBlue = (0,100,160)
sienna = (160,82,45)
white = (255,255,255)
darkGreen = (0,100,0)
darkKhaki = (189,183,107)

red = (200,0,0)
green = (0,200,0)

# Global Variables:
whitePlayer = None
blackPlayer = None
whiteDepth = 1
blackDepth = 1
whiteHeuristic = 0
blackHeuristic = 0
startTime = 0
whiteAITimes = []
blackAITimes = []
turns = 0

# Constants
HUMAN = 0
AI = 1
HEURISTIC_LIST = [
                    "HEURISTICS",
                    "0 - Basic. Considers total piece value and maximizing possible moves",
                    "1 - Hash. Like 0, but stores nextMoves in dictionary",
                    "2 - Basic Sort. Like 0, but sorts nextMoves by highest weight",
                    "3 - NegaMax",
                    "4 - Hash Sort. Unfinished.",
                    "5 - NegaMax Position. Like NegaMax, but uses positional values",
                    "6 - Basic Sort Position. Like Basic Sort, but uses positional values",
                    "7 - Hash Sort Position. Like Hash Sort, but uses positional values. Unfinished",
                    "Other - Moves randomly selected."
                 ]

# Initilizing the display and setting the title of window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess AI Capstone')
clock = pygame.time.Clock()

# Function for text objects
def textObjects(text, font):
    textSurface = font.render(text, True, black) # Color might change with the new color module
    return textSurface, textSurface.get_rect()

# Function for button objects
def button(msg,x,y,w,h,ic,ac,action = None, args = None):
    """Creates Button object
    Uses x and y for start position (top left of button)
    Uses w and h for width and height
    Uses ic for initial color and ac for action color (RGB color tuple)
    Uses action for mouse click action"""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if args == None:
                action()
            else:
                action(args)
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("agencyfb",22)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def square(x,y,w,h,ic,ac,action = None, args = None):
    """Creates square object for game board
    Uses x and y for start position (top left of button)
    Uses w and h for width and height
    Uses ic for initial color and ac for action color (RGB color tuple)
    Uses action for mouse click action"""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if args == None:
                action()
            else:
                action(args)
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

# Helper function for quit/exit button
def quitgame():
    pygame.quit()   
    quit()

# Helper function to restart game
def newGame():
    global selectMoves
    global selectedSpace
    global state
    selectMoves = []
    selectedSpace = None
    state = Board()
    gameIntro()


# Functions for White and Black player selection
def whiteHuman():
    global whitePlayer
    whitePlayer = HUMAN

def whiteAI():
    global whitePlayer
    whitePlayer = AI

def blackHuman():
    global blackPlayer
    blackPlayer = HUMAN

def blackAI():
    global blackPlayer
    blackPlayer = AI

def selectSpace(coords):
    global state
    global selectMoves
    global selectedSpace
    space = state.board[coords[0]][coords[1]]
    if isinstance(space, P.Piece) and state.turn == space.color:
        selectedSpace = coords
        selectMoves = Logic.select_piece(state, coords[0], coords[1])

def selectSpaceHuman(coords):
    global state
    
    if (state.turn == P.WHITE and whitePlayer == HUMAN) or (state.turn == P.BLACK and blackPlayer == HUMAN):    
        selectSpace(coords)

def makeMove(moveCoords):
    global state
    global selectMoves
    global selectedSpace
    global turns
    
    movement = selectMoves[selectMoves.index(moveCoords)]
    
    if state.turn == state.board[selectedSpace[0]][selectedSpace[1]].color:
        newState = Logic.move_piece(state, selectedSpace[0], selectedSpace[1], movement)
        
        if newState == None:
            return
        
        state = newState
        selectedSpace = None
        selectMoves.clear()
    
    turns += 1
    
    #print()
    #print("White Total Piece Val:", state.whiteTotalPieceVal)
    #print("White Pos Piece Val:", state.whitePosPieceVal)
    #print("Black Total Piece Val:", state.blackTotalPieceVal)
    #print("Black Pos Piece Val:", state.blackPosPieceVal)
    #print()

# start button function
def startGame(args):
    global whitePlayer
    global blackPlayer

    # Might need to change this to display constantly if clicked
    # This means i need a variable to toggle it
    if whitePlayer is None or blackPlayer is None:
        text = pygame.font.SysFont("agencyfb",25)
        TextSurf, TextRect = textObjects("Please select Human or AI for both sides", text)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
    elif whitePlayer == 1 and args[0].text == '':
        text = pygame.font.SysFont("agencyfb",25)
        TextSurf, TextRect = textObjects("Please enter a look ahead value for white side AI", text)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
    elif blackPlayer == 1 and args[1].text == '':
        text = pygame.font.SysFont("agencyfb",25)
        TextSurf, TextRect = textObjects("Please enter a look ahead value for black side AI", text)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
    else:
        #STUB might need to fix
        #Add Values for the AI into some sort of check
        gameMain()

def gameIntro():
    global whiteDepth
    global blackDepth
    global whiteHeuristic
    global blackHeuristic
    
    intro = True
    
    # Input textbox initializations
    whiteDepthID = 0
    blackDepthID = 1
    whiteHeurID = 2
    blackHeurID = 3
    
    inputBox1 = InputBox(200, 425, 50, 50, black, red, text=str(whiteDepth), ident=whiteDepthID)
    inputBox2 = InputBox(550, 425, 50, 50, black, red, text=str(blackDepth), ident=blackDepthID)
    inputBox3 = InputBox(275, 425, 50, 50, black, red, text=str(whiteHeuristic), ident=whiteHeurID)
    inputBox4 = InputBox(475, 425, 50, 50, black, red, text=str(blackHeuristic), ident=blackHeurID)
    inputBoxes = [inputBox1, inputBox2, inputBox3, inputBox4]

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            for box in inputBoxes:
                box.handle_event(event)
        for box in inputBoxes:
            box.update()
            if (box.ident == whiteDepthID):
                whiteDepth = int(box)
            elif (box.ident == blackDepthID):
                blackDepth = int(box)
            elif (box.ident == whiteHeurID):
                whiteHeuristic = int(box)
            elif (box.ident == blackHeurID):
                blackHeuristic = int(box)
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("agencyfb",115)
        TextSurf, TextRect = textObjects("Chess AI", largeText)
        TextRect.center = ((display_width/2),(display_height/6))
        gameDisplay.blit(TextSurf, TextRect)

        # Left side text
        text = pygame.font.SysFont("agencyfb",25)
        TextSurf, TextRect = textObjects("White", text)
        TextRect.center = (115,320)
        gameDisplay.blit(TextSurf, TextRect)

        text = pygame.font.SysFont("agencyfb",16)
        TextSurf, TextRect = textObjects("Look Ahead", text)
        TextRect.center = (225,400)
        gameDisplay.blit(TextSurf, TextRect)
        
        text = pygame.font.SysFont("agencyfb",16)
        TextSurf, TextRect = textObjects("Heuristic", text)
        TextRect.center = (300,400)
        gameDisplay.blit(TextSurf, TextRect)

        # Left side buttons - white
        button("Human",65,350,100,50,green,red,whiteHuman)
        button("AI",65,425,100,50,green,red,whiteAI)

        # Left side circles
        # Flow control for which button is selected (1 for hollow, 0 for filled)
        global whitePlayer
        if whitePlayer is None:
            pygame.draw.circle(gameDisplay, black, (35,375), 10, 1)
            pygame.draw.circle(gameDisplay, black, (35,450), 10, 1)
        elif whitePlayer == 0:
            pygame.draw.circle(gameDisplay, black, (35,375), 10, 0)
            pygame.draw.circle(gameDisplay, black, (35,450), 10, 1)
        else:
            pygame.draw.circle(gameDisplay, black, (35,375), 10, 1)
            pygame.draw.circle(gameDisplay, black, (35,450), 10, 0)

        # Center Button
        button("Start",350,500,100,50,green,red,startGame, inputBoxes)

        # Right side text
        text = pygame.font.SysFont("agencyfb",25)
        TextSurf, TextRect = textObjects("Black", text)
        TextRect.center = (685,320)
        gameDisplay.blit(TextSurf, TextRect)

        text = pygame.font.SysFont("agencyfb",16)
        TextSurf, TextRect = textObjects("Look Ahead", text)
        TextRect.center = (575,400)
        gameDisplay.blit(TextSurf, TextRect)

        text = pygame.font.SysFont("agencyfb",16)
        TextSurf, TextRect = textObjects("Heuristic", text)
        TextRect.center = (500,400)
        gameDisplay.blit(TextSurf, TextRect)

        # Right side buttons - Black
        button("Human",635,350,100,50,green,red,blackHuman)
        button("AI",635,425,100,50,green,red,blackAI)
        button("Exit",635,500,100,50,red,green,quitgame)

        # Right side circles
        # Flow control for which button is selected (1 for hollow, 0 for filled)
        global blackPlayer
        if blackPlayer is None:
            pygame.draw.circle(gameDisplay, black, (765,375), 10, 1)
            pygame.draw.circle(gameDisplay, black, (765,450), 10, 1)
        elif blackPlayer == 0:
            pygame.draw.circle(gameDisplay, black, (765,375), 10, 0)
            pygame.draw.circle(gameDisplay, black, (765,450), 10, 1)
        else:
            pygame.draw.circle(gameDisplay, black, (765,375), 10, 1)
            pygame.draw.circle(gameDisplay, black, (765,450), 10, 0)
        for box in inputBoxes:
            box.draw(gameDisplay)

        # Lower Left Heuristic List
        #text = pygame.font.SysFont("agencyfb",16)
        #for i in range(0, len(HEURISTIC_LIST)):
        #    TextSurf, TextRect = textObjects(HEURISTIC_LIST[i], text)
        #    TextRect.topleft = (25, 130 + (i * 16))
        #    gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(15)

def chessPiece(x, y, img):
    gameDisplay.blit(img,(x,y))

def getCords(args):
    for x in args:
        print(args)

def gameInfoText(player, depth, heuristic, xPos, color):
    text = pygame.font.SysFont("agencyfb",22)
    
    TextSurf, TextRect = textObjects("Player: " + color, text)
    TextRect.topleft = (xPos,475)
    gameDisplay.blit(TextSurf, TextRect)
    
    if (player == HUMAN):
        TextSurf, TextRect = textObjects("Type: Human", text)
        TextRect.topleft = (xPos,500)
        gameDisplay.blit(TextSurf, TextRect)
    else:
        TextSurf, TextRect = textObjects("Type: AI", text)
        TextRect.topleft = (xPos,500)
        gameDisplay.blit(TextSurf, TextRect)
        
        TextSurf, TextRect = textObjects("Lookahead: " + str(depth), text)
        TextRect.topleft = (xPos,525)
        gameDisplay.blit(TextSurf, TextRect)
        
        TextSurf, TextRect = textObjects("Heuristic: " + str(heuristic), text)
        TextRect.topleft = (xPos,550)
        gameDisplay.blit(TextSurf, TextRect)

def printResults(checkmate, state):
    endTime = time.perf_counter()
    
    print("\n\n\n")
    print("-------------RESULTS------------")
    print("---Game---")
    end = ""
    if (checkmate == None):
        end = "Stalemate"
    elif (state.whiteChecked and state.blackChecked):
        end = "Somehow both sides won simultaneously. Huh."
    elif (not state.whiteChecked and not state.blackChecked):
        end = "Forfeit"
    elif (state.whiteChecked):
        end = "Black checkmated white"
    elif (state.blackChecked):
        end = "White checkmated black"
    else:
        end = "If you're seeing this, something went really wrong with the program."
    
    print("End State:", end)
    print("Turns Taken:", turns)
    print("Time Taken:", "{0:.{1}f}".format(endTime - startTime, 2), "seconds")
    print()
    
    for side in [P.WHITE, P.BLACK]:
        sideHuman = (side == P.WHITE and whitePlayer == HUMAN) or (side == P.BLACK and blackPlayer == HUMAN)
        print("---" + P.colorToStr(side) + " Side---")
        
        pType = ""
        if (sideHuman):
            pType = "Human"
        else:
            pType = "AI"
        print("Type:", pType)
        
        if (side == P.WHITE):
            print("White Total Piece Val:", state.whiteTotalPieceVal)
            print("White Pos Piece Val:", state.whitePosPieceVal)
        else:
            print("Black Total Piece Val:", state.blackTotalPieceVal)
            print("Black Pos Piece Val:", state.blackPosPieceVal)
        
        if not sideHuman:
            minAITime = 0
            maxAITime = 0
            avgAITime = 0
            
            try:
                if (side == P.WHITE):
                    minAITime = min(whiteAITimes)
                    maxAITime = max(whiteAITimes)
                    avgAITime = statistics.mean(whiteAITimes)
                else:
                    minAITime = min(blackAITimes)
                    maxAITime = max(blackAITimes)
                    avgAITime = statistics.mean(blackAITimes)
                print("Lowest think time:", "{0:.{1}f}".format(minAITime, 2), "seconds")
                print("Highest think time:", "{0:.{1}f}".format(maxAITime, 2), "seconds")
                print("Average think time:", "{0:.{1}f}".format(avgAITime, 2), "seconds")
            except ValueError:
                print("Not enough information to display lowest, highest, and average think times.")
                
        print()
            
            
    

def gameMain():
    global state
    global selectMoves
    global whitePlayer
    global blackPlayer
    global whiteDepth
    global blackDepth
    global whiteHeuristic
    global blackHeuristic
    global startTime
    global whiteAITimes
    global blackAITimes
    global turn
    global turns
    gameExit = False
    checkmate = False
    crash = False
    crashedColor = ""
    printedResults = False
    startTime = time.perf_counter()
    turns = 0
    whiteAITimes.clear()
    blackAITimes.clear()
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not printedResults:
                    printResults(checkmate, state)
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        
        #Left-side Info
        gameInfoText(whitePlayer, whiteDepth, whiteHeuristic, 25, "White")
        
        #Right-side Info
        gameInfoText(blackPlayer, blackDepth, blackHeuristic, 700, "Black")
        
        # Add double for loop to make array of buttons
        for x in range(0, 8):
            for y in range(0, 8):
                if (x,y) in selectMoves:
                    """Highlighted Buttons"""
                    if x % 2 == 0:
                        if y % 2 == 0:
                            square((x * 45 + 220),(435 - y * 45),45,45,darkGreen,darkBlue,makeMove,(x,y))
                        else:
                            square((x * 45 + 220),(435 - y * 45),45,45,darkKhaki,skyBlue,makeMove,(x,y))

                    else:
                        if y % 2 == 0:
                            square((x * 45 + 220),(435 - y * 45),45,45,darkKhaki,skyBlue,makeMove,(x,y))
                        else:
                            square((x * 45 + 220),(435 - y * 45),45,45,darkGreen,darkBlue,makeMove,(x,y))
                else:
                    """Non-Highlighted Buttons"""
                    if x % 2 == 0:
                        if y % 2 == 0:
                            square((x * 45 + 220),(435 - y * 45),45,45,sienna,darkBlue,selectSpaceHuman,(x,y))
                        else:
                            square((x * 45 + 220),(435 - y * 45),45,45,lightGrey,skyBlue,selectSpaceHuman,(x,y))
                    else:
                        if y % 2 == 0:
                            square((x * 45 + 220),(435 - y * 45),45,45,lightGrey,skyBlue,selectSpaceHuman,(x,y))
                        else:
                            square((x * 45 + 220),(435 - y * 45),45,45,sienna,darkBlue,selectSpaceHuman,(x,y))

                if (isinstance(state.board[x][y], P.Piece)):
                    img = pygame.image.load(state.board[x][y].image)
                    chessPiece((x * 45 + 220),(435 - y * 45),img)

        # Printing text to indicate check or checkmate
        if crash:
            text = pygame.font.SysFont("agencyfb",25)
            TextSurf, TextRect = textObjects("Oops, the " + crashedColor + " AI thought of this state, causing a crash.", text)
            TextRect.center = ((display_width/2),(display_height/8))
            gameDisplay.blit(TextSurf, TextRect)
        elif state.whiteChecked:
            if Logic.is_checkmate(state,state.turn) == True or checkmate == True:
                text = pygame.font.SysFont("agencyfb",25)
                TextSurf, TextRect = textObjects("Checkmate! Black Wins!", text)
                TextRect.center = ((display_width/2),(display_height/8))
                gameDisplay.blit(TextSurf, TextRect)
                checkmate = True
            else:
                text = pygame.font.SysFont("agencyfb",25)
                TextSurf, TextRect = textObjects("White is in check", text)
                TextRect.center = ((display_width/2),(display_height/8))
                gameDisplay.blit(TextSurf, TextRect)
        elif state.blackChecked:
            if Logic.is_checkmate(state,state.turn) == True or checkmate == True:
                text = pygame.font.SysFont("agencyfb",25)
                TextSurf, TextRect = textObjects("Checkmate! White Wins!", text)
                TextRect.center = ((display_width/2),(display_height/8))
                gameDisplay.blit(TextSurf, TextRect)
                checkmate = True
            else:
                text = pygame.font.SysFont("agencyfb",25)
                TextSurf, TextRect = textObjects("Black is in check", text)
                TextRect.center = ((display_width/2),(display_height/8))
                gameDisplay.blit(TextSurf, TextRect)
        elif Logic.is_checkmate(state,state.turn) == None or checkmate == None:
            text = pygame.font.SysFont("agencyfb",25)
            TextSurf, TextRect = textObjects("Stalemate. It's a tie.", text)
            TextRect.center = ((display_width/2),(display_height/8))
            gameDisplay.blit(TextSurf, TextRect)
            checkmate = None


        # Buttons for new game or exit after checkmate
        if checkmate == True or checkmate == None or crash:
            button("New Game",165,500,100,50,green,red,newGame)
            button("Exit",535,500,100,50,red,green,quitgame)
            
            if not printedResults:
                printResults(checkmate, state)
                printedResults = True
        

        pygame.display.update()
        clock.tick(15)
        if not crash and ((state.turn == P.WHITE and whitePlayer == AI) or (state.turn == P.BLACK and blackPlayer == AI)) and checkmate != True and checkmate != None:
            # AI Control
            
            depthLim = 0
            heuristic = 0
            if state.turn == P.WHITE:
                depthLim = whiteDepth
                heuristic = whiteHeuristic
            elif state.turn == P.BLACK:
                depthLim = blackDepth
                heuristic = blackHeuristic
            
            try:
                node, thinkTime = aiSearch(state, depthLim, heuristic)
                
                if (state.turn == P.WHITE):
                    whiteAITimes.append(thinkTime)
                else:
                    blackAITimes.append(thinkTime)
                
                selectSpace(node.space)
                makeMove(node.move.space)
            except AI_Exception as a:
                crash = True
                state = a.state
                crashedColor = P.colorToStr(a.aiColor)
                print(a)