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
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def gameIntro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Chess AI", largeText)
        TextRect.center = ((display_width/2),(display_height/4))
        gameDisplay.blit(TextSurf, TextRect)

        #button("GO!",150,450,100,50,green,bright_green,game_loop)
        #button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

gameIntro()