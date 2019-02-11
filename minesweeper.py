import pygame
import board as b
import game as g

pygame.init()

s_width = 500   # Width of screen
s_height = 500  # Height of screen

win = pygame.display.set_mode((s_width, s_height))  # Created window to display game

run = True
while run:
    pygame.time.delay(50)

