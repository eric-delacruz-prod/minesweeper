import pygame
import board as b
import game as g

pygame.init()

s_width = 700   # Width of screen
s_height = 700  # Height of screen
x = 95 # Location of board - x-coord
y = 95 # Location of board - y-coord
NUM_BOMBS = 10 # Number of bombs

window = pygame.display.set_mode((s_width, s_height))  # Created window to display game
window.fill((0, 0, 0))

run = True
# Main game loop
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    x_current = x
    y_current = y
    for i in range(10):
        for j in range(10):
            #if g.getCoordinate(i, j)['cleared']:
            #    pygame.draw.rect(window, (210, 210, 210), (x_current, y_current, 50, 50))
           # else:
                pygame.draw.rect(window, (40, 135, 200), (x_current, y_current, 50, 50))
                x_current += 51
        y_current += 51
        x_current = x

    pygame.display.update()

pygame.quit()
