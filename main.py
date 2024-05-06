import pygame
import sys
import random

#Initialize the pygame
pygame.init()

#Create a screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#Background
background = pygame.image.load('Gray.png')

#Title and icon
pygame.display.set_caption("COLORED LINES")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #RGB value
    screen.fill((0, 0, 0))
    pygame.display.update()


    


