import pygame
import board as b
import game as g
import math

#GLOBALS
s_width = 700   # Width of screen
s_height = 700  # Height of screen
x = 95 # Location of board - x-coord
y = 95 # Location of board - y-coord
NUM_BOMBS = 10 # Number of bombs

#HELPER FUNCTIONS
def convertPygameCoordinates(pygame_x, pygame_y, offset_x, offset_y, width, height):
    '''
    Converts Pygame coordinates to coordinates on the grid.
    @param pygame_x X, given by pygame (ie relative to upper left hand corner of the window.)
    @param pygame_y Y, given by pygame.
    @param offset_x The X coordinate, in the pygame coordinate system, of the upper left hand corner of the grid.
    @param offset_y The Y coordinate, in the pygame coordinate system, of the upper left hand corner of the grid.
    @param width The distance, in terms of pygame coordinates, between grid coordinates in the x direction.
    @param height The distance, in terms of pygame coordinates, between grid coordinates in the y direction.
    @return A tuple containing the X and Y coordinates on the grid. (X, Y)
    @note But how many fence posts did we pass, Freund?
    '''

    inGameX = math.floor((pygame_x-offset_x)/width)
    inGameY = math.floor((pygame_y-offset_y)/height)
    return (inGameX, inGameY)

#GUI

#Start Pygame
pygame.init()
window = pygame.display.set_mode((s_width, s_height))  # Created window to display game
window.fill((0, 0, 0))
pygame.display.set_caption("Minesweeper") # Sets menu bar title

#Initialize Board
g.initialize(x, y, NUM_BOMBS)

run = True
# Main game loop
while run:
    pygame.time.delay(50)

    left_mouse = False
    right_mouse = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = event.pos
            if event.button == 1:
                left_mouse = True
            elif event.button == 3:
                right_mouse = True
        if event.type == pygame.MOUSEMOTION:
            print(convertPygameCoordinates(event.pos[0], event.pos[1], x, y, 50, 50))

    if left_mouse:
        #Do some crap with cPC and event.pos
    elif right_mouse:
        #Same
    '''
    Generates at 10x10 board
    Checks if tile has been "cleared" or "flagged"
    '''
    x_current = x
    y_current = y
    for i in range(10):
        for j in range(10):
            if g.getCoordinate(i, j)['cleared']:
                pygame.draw.rect(window, (210, 210, 210), (x_current, y_current, 50, 50))
            if g.getCoordinate(i, j)['flagged']:
                pygame.draw.rect(window, (40, 135, 200), (x_current, y_current, 50, 50))
            # Draws circles to be used as flags
                pygame.draw.circle(window, (190, 40, 37), (x_current + 25, y_current + 25), 10, 0)
            else:
                pygame.draw.rect(window, (40, 135, 200), (x_current, y_current, 50, 50))
                x_current += 51
        y_current += 51
        x_current = x

    # Ends game if ESC is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    pygame.display.update()

pygame.quit()

