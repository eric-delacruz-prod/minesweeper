#import pygame library from https://www.pygame.org/, used documentation from https://www.pygame.org/docs/ as reference
import pygame
import board as b
import game as g
import math
import time
import random
import sys

#GLOBALS

OFFSET_X = 0 # Location of board - x-coord
OFFSET_Y = 0 # Location of board - y-coord
TILES_X = 20 #Number of tiles in the x direction
TILES_Y = 20 #Number of tiles in the y direction
BORDER = 1 #The size, in pixels, of the border between squares.
NUM_BOMBS = 10 # Number of bombs
NUM_FLAGS = 10 # Number of flags
NUM_TILES = 100 # Number of total tiles
SHOW_BOMBS = False #Whether bombs should be shown.
SHOW_NUMS  = False #Whether adjacent numbers should be shown.
EXPLOSION_TIME = 0 #How many frames between explosions on game over. Do you dare set it to 0?
NUMBER_EXPLOSIONS = 20 #How many explosions occur on game over.
SONG_END = pygame.USEREVENT + 1 #for the custom music event 
stoptime = False #Whether the game has ended for time
pygame.mixer.init(44100, -16,2,2048) #initialized mixer
#HANDLE USER VARIABLES
#Handle input from the command line. Valid formats are:
#-No arguments (which leaves TILES_X and TILES_Y as they are)
#-<bombs> <width/height>
#-<bombs> <width> <height>
try:
    user_bombs = 0
    user_height = 0
    user_width = 0
    args = sys.argv
    if len(args) == 1:
        #No arguments specified (except for the file, of course ;) )
        user_bombs = NUM_BOMBS
        user_height = TILES_Y
        user_width = TILES_X
    elif len(args) == 3:
        #When two arguments are specified.
        user_bombs = int(args[1])
        user_height = int(args[2])
        user_width = user_height
    elif len(args) == 4:
        #When three arguments are specified.
        user_bombs = int(args[1])
        user_height = int(args[3])
        user_width = int(args[2])
    else:
        raise Exception

    assert user_height > 1
    assert user_width > 1
    assert (user_bombs >= 1) and (user_bombs < (user_height * user_width))
    NUM_BOMBS = user_bombs
    NUM_FLAGS = user_bombs
    TILES_X = user_width
    TILES_Y = user_height
    NUM_TILES = TILES_X * TILES_Y

except:
    print("USAGE: ")
    print("python minesweeper.py")
    print("python minesweeper.py <number of bombs> <number of tiles in x and y directions>")
    print("python minesweeper.py <number of bombs> <number of tiles in x direction> <number of tiles in y direction>")
    sys.exit() 

#Assertations regarding game size. There is a maximum game size.
assert TILES_X <= 30, "Game is too large. Maximum size is 30."
assert TILES_Y <= 30, "Game is too large. Maximum size is 30."

#DO MATH WITH SCREEN SIZE
SCREEN_X = 30*TILES_X # Width of screen
SCREEN_Y = 30*TILES_Y # Height of screen
GAME_SIZE_X = 30*TILES_X #The size, in pixels, of the playing area in the x direction
GAME_SIZE_Y = 30*TILES_Y #The size, in pixels, of the playing area in the y direction
tile_width = (GAME_SIZE_X-(TILES_X*BORDER))/TILES_X
tile_height = tile_width
explosionFrame = 0

#HELPER FUNCTIONS
def gameWon(Tiles_X, Tiles_Y, NUM_BOMBS, rev_tiles):
    '''
    Determines whether the game meets the win condition of minesweeper
    @param Tiles_X: Number of tiles in X direction
    @param Tiles_Y: Number of tiles in Y direction
    @param NUM_BOMBS: Total bombs in the game
    @param rev_tiles: Number of revealed tiles being counted in game.py (must use g.rev_tiles)
    @return: Boolean of True if condition is met
    '''
    total = Tiles_X * Tiles_Y - NUM_BOMBS
    if rev_tiles == total:
        return True
    
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

def gameOver():
    '''
    Puts a randomly colored circles on the screen, which sorta kinda look like an explosion
    '''
    global window
    random_x = random.randrange(0, SCREEN_X)
    random_y = random.randrange(0, SCREEN_Y)
    random_r = random.randrange(30, 300)
    random_c = (255, random.randrange(0, 255), random.randrange(0, 20))
    pygame.draw.circle(window, random_c, (random_x, random_y), random_r)

#plays piano after win/lose
def endMusic():
    '''
    Toggles the music off after the completion of the game
    '''
    global onlyTriggerOnce
    if onlyTriggerOnce:
        pygame.mixer.music.fadeout(750)
        play_next_song(7)
        onlyTriggerOnce = False

#called after a song ends
def play_next_song(index):
    '''
    Looping through song clips
    '''
    global _songs
    pygame.mixer.music.load(_songs[index])
    pygame.mixer.music.play()

#Start Pygame
#pre_init sets the sampleRate, num channels, buffersize.
pygame.mixer.pre_init(48000, 16, 2, 1024) #Initializes the mixer for the music
pygame.init() #Starts pygame
window = pygame.display.set_mode((SCREEN_X, SCREEN_Y+(30) ))  # Created window to display game
window.fill((0, 0, 0)) #Makes the screen be black.
pygame.display.set_caption("Minesweeper") # Sets menu bar title
pygame.font.init() #Starts the font engine.


#Initialize Board
g.initialize(TILES_X, TILES_Y, NUM_BOMBS) #This is a game.py functionality, it sets up the board.

run = True #This controls the main game loop.
#Main game loop. The program does this over and over, drawing things to the screen repeatedly.
#Tiles are rectangles, drawn to the screen. Flags and bombs are just circles. Text (ie, for the numbers surrounding the bombs) are surface objects containing text.

x_mouse = 0  # Setting x and y mouse coordinates prior to game run prevents x_mouse not defined error
y_mouse = 0
game_progress = 0

#Here are the necessary inits for music files
_songs = ['marchEightTeen-INTRO.wav','marchEightTeen-PART1.wav','marchEightTeen-PART2.wav','marchEightTeen-PART3.wav','marchEightTeen-PART4.wav','marchEightTeen-PART5.wav','marchEightTeen-PART6.wav','marchEightTeen-FINAL.wav']
#Define an event that triggers when the song finishes
pygame.mixer.music.set_endevent(SONG_END)
#load and play the very first section immediately
pygame.mixer.music.load(_songs[0])
pygame.mixer.music.play(0)
#This bool is disgusting programming style, but I don't know how to get around the end game condition without it.
onlyTriggerOnce = True


t0 = time.time()
while run:

    #pygame.time.delay(50) #This makes sure that the game doesn't run too fast. Disable at your own risk!
  
    #This is used for determining which parts of the music track should be playing.
    completionStatus = g.rev_tiles / (NUM_TILES - NUM_BOMBS)
 
    #We set up the left and right mouse buttons to default to not pressed.
    left_mouse = False
    mid_mouse = False
    right_mouse = False   

    #Check for things that have happened.
    for event in pygame.event.get(): #pygame.event.get gets a LIST of EVENTS. You can see this in action by printing these to the screen.
        if event.type == pygame.QUIT: #This is what occurs when you press the "x" button.
            run = False #When the user x's out, we stop the loop.
        #The following plays the appropritate section of the track based on the percentage complete. 
        if event.type == SONG_END and onlyTriggerOnce:
            if completionStatus < .16:  
                play_next_song(1)
            elif completionStatus < .32:
                play_next_song(2)
            elif completionStatus < .48:
                play_next_song(3)
            elif completionStatus < .64:
                play_next_song(4)
            elif completionStatus < .8:
                play_next_song(5)
            else:
                play_next_song(6)
        if pygame.key.get_pressed() [pygame.K_c] == True:
            mid_mouse = True
        if event.type == pygame.MOUSEBUTTONDOWN: #Check for pressing a mouse button.
            if event.button == 1: #1 is left click. We set the left click flag to true.
                left_mouse = True
            elif event.button == 2:
                mid_mouse = True
            elif (event.button == 3):#3 is right click. (Think Left, Middle, Right)
                right_mouse = True
                x_mouse, y_mouse = convertPygameCoordinates(event.pos[0], event.pos[1], OFFSET_X, OFFSET_Y, tile_width+BORDER, tile_height+BORDER) #This function converts PYGAME coordinates to GRID coordinates. See it's documentation for more...
            
                #Number of flags does not matter anymore
                '''''
                if (NUM_FLAGS == 0) and (g.myBoard.getFlagged(x_mouse, y_mouse) == False):
                    right_mouse = False
                elif (NUM_FLAGS > 0) and (g.myBoard.getFlagged(x_mouse, y_mouse) == False):
                    NUM_FLAGS -= 1
                else:
                     NUM_FLAGS += 1  
                '''''              
                #print(NUM_FLAGS) #for debugging purposes
        if event.type == pygame.MOUSEMOTION: #Check to see if the mouse has moved.
            x_mouse, y_mouse = convertPygameCoordinates(event.pos[0], event.pos[1], OFFSET_X, OFFSET_Y, tile_width+BORDER, tile_height+BORDER) #This function converts PYGAME coordinates to GRID coordinates. See it's documentation for more...
    
    #Handle mouse clicks. We include a try/except block to check for index out of range errors (when you click off the board).
    try:
        if left_mouse:
            g.leftClick(x_mouse, y_mouse)
        elif mid_mouse:
            SHOW_BOMBS = not SHOW_BOMBS
            SHOW_NUMS  = not SHOW_NUMS
        elif right_mouse:
            g.rightClick(x_mouse, y_mouse)
    except IndexError:
        pass
    
    #Generate the board
    fontSize = math.floor((tile_height * 1.5))  #Get font size based on the tile size. 
    tileFont = pygame.font.SysFont("", fontSize) #We get the font object. We use pygames "default" font.

    x_current = OFFSET_X #x_current and y_current are pygame coordiates of the grid coordinates that we are drawing. We start at the offset. 
    y_current = OFFSET_Y
    for j in range(TILES_Y): #i, j represent grid x and y respectively.
        for i in range(TILES_X):
            #Draw the tile.
            #NOTE: getCoordinate is a game.py function that returns a dictionary object, with booleans containing different states.
            if g.getCoordinate(i, j)['cleared']: #For example, in this conditional, we check to see if the current tile is cleared.
                pygame.draw.rect(window, (255, 255, 255), (x_current, y_current, tile_width, tile_height)) #If it is cleared, we draw a white rectangle 
                num = g.getCoordinate(i, j)['surrounding'] #There is also an element of the returned dictionary, surrounding. This key contains the number of bombs surrounding the tile.
                #Show the number of bombs surrounding the position.
                if num != 0: #We don't want to print anything is num == 0 (As this would clutter the screen)
                    tileNum = tileFont.render(str(num), 1, (0, 0, 0))
                    window.blit(tileNum, (x_current + (tile_width/5), y_current))
            elif SHOW_NUMS:
                pygame.draw.rect(window, (255, 255, 255), (x_current, y_current, tile_width, tile_height))
                num = g.getCoordinateForCheating(i, j)
                if num != 0:
                    tileNum = tileFont.render(str(num), 1, (0, 0, 0))
                    window.blit(tileNum, (x_current + (tile_width/5), y_current)) 
            elif i == x_mouse and j == y_mouse: #Highlight the current square.
                pygame.draw.rect(window, (100, 100, 100), (x_current, y_current, tile_width, tile_height))
            else: #Draw an uncleared square.
                pygame.draw.rect(window, (40, 135, 200), (x_current, y_current, tile_width, tile_height))
            
            #Draw flag/bomb as a circle. Flags take precedance.
            if g.getCoordinate(i, j)['flagged']:         
                    center_x = int(x_current+(tile_width/2))
                    center_y = int(y_current+(tile_height/2))
                    pygame.draw.circle(window, (255, 0, 0), (center_x, center_y), int(min(tile_height, tile_width)/4))
            elif g.getCoordinate(i, j)['bomb'] and SHOW_BOMBS:
                center_x = int(x_current+(tile_width/2))
                center_y = int(y_current+(tile_height/2))
                pygame.draw.circle(window, (0, 0, 0), (center_x, center_y), int(min(tile_height, tile_width)/4))

            x_current += tile_width + BORDER #Increment the current position by the width of the tile, and the border. Keep in mind that this is the upper left-hand corner of the next tile that will be drawn.
        y_current += tile_height + BORDER #Like the preceding statement, we increment by the border and the height. Keep in mind that increasing y is downward.
        x_current = OFFSET_X #Reset the current x coordinate to the origin.

        #timer part, display the timer under the main window
        if stoptime == False: 
            t1 = time.time()
            endtime = t1-t0
        fontSize = math.floor((tile_height * 1.5))
        objective = str(round(endtime, 2))
        timeFont = pygame.font.SysFont("", fontSize)
        timeMsg = timeFont.render(objective, True, (255, 255, 255))
        #helpMsg = text_objects('chect mode: press',115)
        #surf = pygame.Surface((100, 100))
        #surf.fill((255, 255, 255))
        #window.fill((0, 0, 0)) #Makes the screen be black.
        #pygame.draw.rect(window, (0, 0, 0), (SCREEN_X, 10), SCREEN_Y)
        pygame.draw.rect(window, (0, 0, 0), (0, (SCREEN_Y), SCREEN_X, (30)))
        window.blit(timeMsg, ((SCREEN_X-(SCREEN_X/2)-35), SCREEN_Y + 0))
        #window.blit(helpMsg, ((SCREEN_X-(SCREEN_X/2)-35), SCREEN_Y + 0))
    
    # Ends game if ESC is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    #Handle death.
    if g.isDead:
        endMusic()
        stoptime = True
        loseFont = pygame.font.SysFont("", 5*TILES_X)
        loseMsg = loseFont.render("GAME OVER!", 1, (175, 0, 0))
        window.blit(loseMsg, (SCREEN_X/6, SCREEN_Y/3))
        # Press ESC message
        escFont = pygame.font.SysFont("", 2 * TILES_X)
        escMsg = escFont.render("ESC to quit", 1, (175, 0, 0))
        window.blit(escMsg, (SCREEN_X / 3, SCREEN_Y / 2))
        if explosionFrame > EXPLOSION_TIME and NUMBER_EXPLOSIONS > 0:
            gameOver()
            explosionFrame = 0
            NUMBER_EXPLOSIONS-=1
        explosionFrame+=1
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        SHOW_BOMBS = True
        

    #Handle Win.
    if gameWon(TILES_X, TILES_Y, NUM_BOMBS, g.rev_tiles):
        endMusic()
        winFont = pygame.font.SysFont("", 5*TILES_X)
        winMsg = winFont.render("YOU WIN!", True, (0, 175, 0))
        window.blit(winMsg, (SCREEN_X/4.4, SCREEN_Y/4))
        if stoptime == False:
            t1 = time.time()
            endtime = t1-t0
            stoptime = True
        objective = "TIME: " + str(round(endtime, 2))
        endtimeFont = pygame.font.SysFont("", 3*TILES_X)
        endtimeMsg = endtimeFont.render(objective, True, (0, 175, 0))
        window.blit(endtimeMsg, (SCREEN_X/3, SCREEN_Y/2.5))
        # Press ESC message
        escFont = pygame.font.SysFont("", 2 * TILES_X)
        escMsg = escFont.render("ESC to quit", 1, (0, 175, 0))
        window.blit(escMsg, (SCREEN_X / 2.6, SCREEN_Y / 2))

    pygame.display.flip()
print("Quitted gracefully.")
pygame.quit() #If the main game loop breaks, we quit.

