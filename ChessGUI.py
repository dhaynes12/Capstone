# Created by Devan and David
# For use in Chess AI Program

# Will contain the main portion of the GUI

import pygame
import time
import random # probably dont need
from InputBox import *
import os
 
pygame.init() # Wont need later because main should have

# Display dimention -- Will need to change to match screen
display_width = 800
display_height = 600

# Some basic colors
black = (0,0,0)
darkGrey = (55,55,55)
lightGrey = (235,235,235)
skyBlue = (176,248,255)
darkBlue = (0,100,160)
sienna = (160,82,45)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

# Global Variables:
# 0 for human, 1 for AI
whitePlayer = None
blackPlayer = None

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

def square(msg,x,y,w,h,ic,ac,action = None, args = None):
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
    smallText = pygame.font.SysFont("agencyfb",22)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

# Helper function for quit/exit button
def quitgame():
    pygame.quit()
    quit()

# Functions for White and Black player selection
def whiteHuman():
    global whitePlayer
    whitePlayer = 0

def whiteAI():
    global whitePlayer
    whitePlayer = 1

def blackHuman():
    global blackPlayer
    blackPlayer = 0

def blackAI():
    global blackPlayer
    blackPlayer = 1

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

    intro = True
    
    # Input textbox initializations
    inputBox1 = InputBox(200, 425, 50, 50, black, red)
    inputBox2 = InputBox(550, 425, 50, 50, black, red)
    inputBoxes = [inputBox1, inputBox2]

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            for box in inputBoxes:
                box.handle_event(event)
        for box in inputBoxes:
            box.update()        
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("agencyfb",115)
        TextSurf, TextRect = textObjects("Chess AI", largeText)
        TextRect.center = ((display_width/2),(display_height/6))
        gameDisplay.blit(TextSurf, TextRect)

        # Left side buttons - white
        button("Human",65,350,100,50,green,red,whiteHuman) # still need function for toggle with other button
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

        pygame.display.update()
        clock.tick(15)

def chessPiece(x, y, img):
    gameDisplay.blit(img,(x,y))

def gameMain():
    gameExit = False
    blackBishop = pygame.image.load("pieces\\black_bishop.png")
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        # Add double for loop to make array of buttons
        for x in range(0, 8):
            for y in range(0, 8):
                if x % 2 == 0:
                    if y % 2 == 0:
                        square("",(x * 45 + 220),(435 - y * 45),45,45,sienna,darkBlue,blackAI)
                    else:
                        square("",(x * 45 + 220),(435 - y * 45),45,45,lightGrey,skyBlue,blackAI)
                else:
                    if y % 2 == 0:
                        square("",(x * 45 + 220),(435 - y * 45),45,45,lightGrey,skyBlue,blackAI)
                    else:
                        square("",(x * 45 + 220),(435 - y * 45),45,45,sienna,darkBlue,blackAI)
        
        chessPiece(220,435,blackBishop)

        pygame.display.update()
        clock.tick(15)
    #TODO make main gameboard

# Make sure to remove this after
#gameIntro()
gameMain()
