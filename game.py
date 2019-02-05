#Minesweeper Game Logic
import board as b

myBoard = b.Board(1, 1)#The global board object. The real values should be set in initialize.

def initialize(x_size, y_size):
    '''
    Initializes a new board, and randomizes the placement of bombs within the board.
    @param x_size The size of the board in the x direction.
    @param y_size The size of the board in the y direction.
    @throw IndexError if x_size or y-size is less than or equal to one, which doesn't make sense, silly.
    '''
    global myBoard

    if y_size <= 1:
        raise IndexError(f"Requested value of y_size ({y_size}) is too small.")
    if x_size <= 1:
        raise IndexError(f"Requested value of x_size ({x_size}) is too small.")
    
    myBoard = b.Board(x_size, y_size)

def click(x, y):
    '''
    What happens on a click of a praticular square. All game logic is handled when this function is called.
    @param x The x coordinate of the square that is clicked.
    @param y The y coordinate of the square that is clicked.
    @throw IndexError if requested coordinate is off the board.
    '''
    global myBoard
    raise NotImplementedError

def getCoordinate(x, y):
    '''
    Get the state of the tile at the given coordinate.
    @param x The x coordinate of the square that is clicked.
    @param y The y coordinate of the square that is clicked.
    @throw IndexError if requested coordinate is off the board.
    @return A dictionary containing boolean values of the three states: "flagged", "cleared", and "bomb". If cleared, an additional field, "surrounding" will have the number of bombs surrounding the location.
    '''
    global myBoard
    raise NotImplementedError

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
        print(f"Clicking at {x}, {y}.\n")
