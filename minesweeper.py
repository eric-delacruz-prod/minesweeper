import pygame
import board as b
import game as g
import math

#GLOBALS
SCREEN_X = 700   # Width of screen
SCREEN_Y = 700  # Height of screen
OFFSET_X = 95 # Location of board - x-coord
OFFSET_Y = 95 # Location of board - y-coord
TILES_X = 3 #Number of tiles in the x direction
TILES_Y = 3 #Number of tiles in the y direction
GAME_SIZE_X = 500 #The size, in pixels, of the playing area in the x direction
GAME_SIZE_Y = 500 #The size, in pixels, of the playing area in the y direction
BORDER = 1 #The size, in pixels, of the border between squares.
NUM_BOMBS = 1 # Number of bombs

tile_width = (GAME_SIZE_X-(TILES_X*BORDER))/TILES_X
tile_height = (GAME_SIZE_Y-(TILES_Y*BORDER))/TILES_Y

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
window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))  # Created window to display game
window.fill((0, 0, 0))
pygame.display.set_caption("Minesweeper") # Sets menu bar title

#Initialize Board
g.initialize(TILES_X, TILES_Y, NUM_BOMBS)

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
            print(convertPygameCoordinates(event.pos[0], event.pos[1], OFFSET_X, OFFSET_Y, tile_height+BORDER, tile_width+BORDER))

    if left_mouse:
        print("hay")
    elif right_mouse:
        print("yo")
    '''
    Generates at 10x10 board
    Checks if tile has been "cleared" or "flagged"
    '''
    x_current = OFFSET_X
    y_current = OFFSET_Y
    for i in range(TILES_X):
        for j in range(TILES_Y):
            if g.getCoordinate(i, j)['cleared']:
                pygame.draw.rect(window, (210, 210, 210), (x_current, y_current, tile_width, tile_height))
            if g.getCoordinate(i, j)['flagged']:
                pygame.draw.rect(window, (40, 135, 200), (x_current, y_current, tile_width, tile_height))
                # Draws circles to be used as flags
                pygame.draw.circle(window, (190, 40, 37), (x_current + (tile_width/2), y_current + (tile_height/2)), 10, 0)
            else:
                pygame.draw.rect(window, (40, 135, 200), (x_current, y_current, tile_width, tile_height))
                x_current += tile_width + BORDER
        y_current += tile_height + BORDER
        x_current = OFFSET_X
    # Ends game if ESC is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    pygame.display.update()

pygame.quit()

