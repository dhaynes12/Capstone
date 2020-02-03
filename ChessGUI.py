# Created by Devan and David
# For use in Chess AI Program

# Will contain the main portion of the GUI

import pygame
import time
import random # probably dont need
 
pygame.init() # Wont need later because main should have

# Display dimention -- Will need to change to match screen
display_width = 800
display_height = 600

# Some basic colors
black = (0,0,0)
white = (255,255,255)

red = (200,0,0)
green = (0,200,0)

# Initilizing the display and setting the title of window
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess AI Capstone')
clock = pygame.time.Clock()

# Function for text objects
def text_objects(text, font):
    textSurface = font.render(text, True, black) # Color might change with the new color module
    return textSurface, textSurface.get_rect()

# Function for button objects
def button(msg,x,y,w,h,ic,ac,action=None):
    """Creates Button object
    Uses x and y for start position (top left of button)
    Uses w and h for width and height
    Uses ic for initial color and ac for action color (RGB color tuple)
    Uses action for mouse clicl action"""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

# Helper function for quit/exit button
def quitgame():
    pygame.quit()
    quit()

def gameIntro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("agencyfb",115)
        TextSurf, TextRect = text_objects("Chess AI", largeText)
        TextRect.center = ((display_width/2),(display_height/6))
        gameDisplay.blit(TextSurf, TextRect)

        # TODO: figure out what side is white and black
        # Left side buttons
        button("Human",65,350,100,50,green,red,quitgame) # still need function for toggle with other button
        button("AI",65,425,100,50,green,red,quitgame)

        # Center Button
        button("Start",350,500,100,50,green,red,quitgame)

        # Right side buttons
        button("Human",635,350,100,50,green,red,quitgame)
        button("AI",635,425,100,50,green,red,quitgame)
        button("Exit",635,500,100,50,red,green,quitgame)

        pygame.display.update()
        clock.tick(15)

gameIntro()