#Minesweeper Game Logic
import board as b
import random

myBoard = b.Board(1, 1)#The global board object. The real values should be set in initialize.
BOMBS = 0
rev_tiles = 0


def initialize(x_size, y_size, bombs):
    '''
    Initializes a new board, and randomizes the placement of bombs within the board.
    @param x_size The size of the board in the x direction.
    @param y_size The size of the board in the y direction.
    @throw IndexError if x_size or y-size is less than or equal to one, which doesn't make sense, silly.
    '''
    global myBoard, BOMBS, isDead
    BOMBS = bombs
    isDead = False
    if y_size <= 1:
        raise IndexError(f"Requested value of y_size ({y_size}) is too small.")
    if x_size <= 1:
        raise IndexError(f"Requested value of x_size ({x_size}) is too small.")
    
    myBoard = b.Board(x_size, y_size)

    #Place bombs
    for i in range(BOMBS):
        while True:
            #Get a random x and y
            random_x = random.randrange(0, x_size)
            random_y = random.randrange(0, y_size)

            if myBoard.getBomb(random_x, random_y): #Test to see if the randomly chosen coordinate is already a bomb.
                continue #If it IS a bomb, we go back to the start of the while loop.
            
            myBoard.setBomb(random_x, random_y, True) #If there is no bomb there, we set a bomb.
            break #We then break out of the while loop.

def rec_reveal(x, y):
    '''
    Reveals spaces after a left click. By checking all
    surrounding spaces and determining if they are also
    in need of revealing we continue until there is no
    direction that is valid to reveal
    @param x The x coordinate of the square that is left clicked.
    @param y The y coordinate of the square that is left clicked.
    '''
    global isDead
    global myBoard
    global rev_tiles
    # Check that space is not cleared, not a bomb,and not dead.
    # Also covers case if there is a bomb and it is flagged we
    # simply return
    if not(myBoard.getFlagged(x, y)) and not(myBoard.getCleared(x, y)) and not(myBoard.getBomb(x, y)) and not isDead:
        # clear the spot since it was clicked and
        # is in a state that is allowed to be cleared
        myBoard.setCleared(x, y, True, False)
        rev_tiles += 1  # Increments tiles revealed for win condition

        # spot is already clear, but now check if
        # its an end point for this reveal branch
        if _getBombsAroundTile(x, y) != 0:
            return
        # spot cleared and is a blank space so search around it
        # begin process over again for each surrounding square
        # in range
        coordsList = myBoard.getSurrounding(x, y)
        for i in coordsList:
            rec_reveal(i[0], i[1])

def leftClick(x, y):
    '''
    Will invoke a recursive reveal function if the spot clicked
    is not flagged and not a bomb, otherwise the isDead is set
    to true if a bomb is clicked
    @param x: The x coordinate of the square that is left clicked.
    @param y: The y coordinate of the square that is left clicked.
    @return: none
    '''
    global myBoard, isDead
    if myBoard.getFlagged(x, y):
        pass
    elif myBoard.getCleared(x, y):
        pass
    elif myBoard.getBomb(x, y):
        isDead = True
    elif not myBoard.getCleared(x, y):
        rec_reveal(x, y)
        myBoard.setCleared(x, y, True)


def rightClick(x, y):
    '''
    What happens on a RIGHT click of a particular square. Toggles flagged state stored within dictionary at location (x,y)
    in myBoard.
    @param x: The x coordinate of the square that is right clicked.
    @param y: The y coordinate of the square that is right clicked.
    @return: none
    '''
    global myBoard
    if not myBoard.getCleared(x, y):
        myBoard.setFlagged(x, y, not myBoard.getFlagged(x, y))  # toggles the flagged states at (x,y) true->false or false->true

def getCoordinate(x, y):
    '''
    Get the state of the tile at the given coordinate.
    @param x The x coordinate of the square that is clicked.
    @param y The y coordinate of the square that is clicked.
    @throw IndexError if requested coordinate is off the board.
    @return A dictionary containing boolean values of the three states: "flagged", "cleared", and "bomb". If cleared, an additional field, "surrounding" will have the number of bombs surrounding the location.
    '''
    global myBoard
    theTile = myBoard.getTile(x, y) #This is already formatted as a dictionary, in the same format as requested.
    if theTile['cleared']: #Append the additional 'surrounding' key if cleared is true.
        theTile['surrounding'] = _getBombsAroundTile(x, y)
    return theTile

def _getBombsAroundTile(x, y):
    '''
    PRIVATE: Get the number of bombs surrounding the given tile.
    @param x The x coordinate to check around.
    @param y The y coordinate to check around. 
    @return The number of bombs surrounding the given coordinate.
    '''
    global myBoard
    coordsSurrounding = myBoard.getSurrounding(x, y) #Get a list of the coordinates surrounding.
    numberOfBombs = 0
    #Check each coordinate.
    for i in coordsSurrounding:
        if myBoard.getBomb(i[0], i[1]):
            numberOfBombs+=1
    return numberOfBombs

def _display():
    '''
    PRIVATE: Displays the board on the command line, along with an interactive shell, without needing a GUI. For testing purposes only.
    '''
    global myBoard
    while True:
        #Show on screen
        for y in range(myBoard.y_size):
            printThis = ""
            for x in range(myBoard.x_size):
                if myBoard.getBomb(x, y):
                    printThis+="B"
                elif myBoard.getCleared(x, y):
                    printThis+=" "
                elif myBoard.getFlagged(x, y):
                    printThis+="F"
                else:
                    printThis+="."
            print(printThis)
        
        #Get "click"
        selection = input("> ")
        x = int(selection.split(',')[0])
        y = int(selection.split(',')[1])
        print(f"Right Clicking at {x}, {y}.\n")
        rightClick(x, y)
