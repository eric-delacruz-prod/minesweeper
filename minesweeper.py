import pygame
import board as b
import game as g

pygame.init()

s_width = 700   # Width of screen
s_height = 700  # Height of screen
x = 150 # Location of board - x-coord
y = 150 # Location of board - y-coord

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
    for i in range(1, 9):
        for j in range(1, 9):
            pygame.draw.rect(window, (255, 255, 255), (x_current, y_current, 50, 50))
            x_current += 51
        y_current += 51
        x_current = x

    # pygame.draw.rect(window, (255, 255, 255), (x, y, 300, 300))
    pygame.display.update()

pygame.quit()
