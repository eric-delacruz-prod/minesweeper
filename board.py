#Minesweeper Board

class Board():
    def __init__(self, x_size, y_size):
        '''
        Sets up the board.
        @param x_size The size of the board along the x-axis.
        @param y_size The size of the board along the y-axis.
        '''

        #Member Variables
        self.x_size = x_size
        self.y_size = y_size

        #Set up the 'field'
        self.field = []
        for x in range(x_size):
            for y in range(y_size):
                entry = {
                    'flagged': False, #Whether or not the user has marked this location as a bomb.
                    'cleared': False, #Whether or not the user has clear this location.
                    'bomb': False, #Whether or not this location contains a bomb.
                }
                self.field.append(entry)

    def getTile(self, x, y):
        '''
        Returns the dictionary associated with the given coordinate.
        @param x The x coordinate.
        @param y The y coordinate.
        @return The dictionary at the given coordinate.
        @throw IndexError if either x or y falls out of bounds.
        '''
        if x > self.x_size or x < 0:
            raise IndexError(f"The given x coordinate {x} is outside of the bounds of the x-axis (Maximum: {self.x_size-1}).")
        elif y > self.y_size or y < 0:
            raise IndexError(f"The given y coordinate {y} is outside of the bounds of the y-axis (Maximum: {self.y_size-1}).")
        else:
            return self.field[x+(self.x_size*y)]
    
    def setFlagged(self, x, y, status):
        '''
        Sets the location at (x, y) to be either flagged or unflagged, dependent upon status.
        @param x The x coordinate.
        @param y The y coordinate.
        @param status If true, set flagged to true. If false, set flagged to false.
        @throw KeyError If the coordinate at (x, y) is cleared. A Cleared tile may not be set to flagged.
        '''
        if self.getCleared(x, y):
            raise KeyError(f"The coordinate ({x},{y}) is cleared, and therefore may not be set to flagged.")
        self._setValue(x, y, status, 'flagged')
        
    def setBomb(self, x, y, status):
        '''
        Sets the location at (x, y) to be either have a bomb or not have a bomb, dependent upon status.
        @param x The x coordinate.
        @param y The y coordinate.
        @param status If true, set bomb to true. If false, set bomb to false.
        @throw KeyError If the coordinate at (x, y) is cleared. A Cleared tile may not be set to bombed.
        '''
        if self.getCleared(x, y):
            raise KeyError(f"The coordinate ({x},{y}) is cleared, and therefore may not be set to bombed.")
        self._setValue(x, y, status, 'bomb')

    def setCleared(self, x, y, status, safe=True):
        '''
        Sets the location at (x, y) to be either be cleared or not be cleared, dependent upon status.
        @param x The x coordinate.
        @param y The y coordinate.
        @param safe If set to True, this will raise an error if attempting to set a flagged tile to cleared.
        @param status If true, set cleared to true. If false, set cleared to false.
        @throw KeyError If the coordinate at (x, y) is flagged if safe is true. A flagged tile may not be set to cleared if safe is true.
        '''
        if self.getFlagged(x, y) and safe:
            raise KeyError(f"The coordinate ({x},{y}) is flagged, and therefore may not be set to cleared. To disable this functionality, set the safe parameter to False.")
        self._setValue(x, y, status, 'cleared')

    def getFlagged(self, x, y):
        '''
        Gets whether or not the given coordinate has been flagged.
        @param x The x coordinate.
        @param y The y coordinate.
        @return True if (x, y) is flagged, False otherwise.
        '''
        return self.getTile(x, y)['flagged']
    
    def getBomb(self, x, y):
        '''
        Gets whether or not the given coordinate has been bombed.
        @param x The x coordinate.
        @param y The y coordinate.
        @return True if (x, y) is bombed, False otherwise.
        '''
        return self.getTile(x, y)['bomb']

    def getCleared(self, x, y):
        '''
        Gets whether or not the given coordinate has been cleared.
        @param x The x coordinate.
        @param y The y coordinate.
        @return True if (x, y) is cleared, False otherwise.
        '''
        return self.getTile(x, y)['cleared']
    
    def getSurrounding(self, x, y):
        '''Gets a list of all coordinates surrounding the given coordinate, excluding all those that lie out of bounds.
        @param x The x coordinate.
        @param y The y coordinate.
        @return A list of tuples. The 0th element of each tuple is the x coordinate, and the 1st element is the y coordinate.
        '''
        inRange = lambda x, y: (x>=0) and (x<self.x_size) and (y>=0) and (y<self.y_size) #A lambda is like a mini-function
        toReturn = []
        if inRange(x-1, y-1):
            toReturn.append((x-1, y-1))
        if inRange(x, y-1):
            toReturn.append((x, y-1))
        if inRange(x+1, y-1):
            toReturn.append((x+1, y-1))
        if inRange(x-1, y):
            toReturn.append((x-1, y))
        if inRange(x+1, y):
            toReturn.append((x+1, y))
        if inRange(x-1, y+1):
            toReturn.append((x-1, y+1))
        if inRange(x, y+1):
            toReturn.append((x, y+1))
        if inRange(x+1, y+1):
            toReturn.append((x+1, y+1))
        
        return toReturn
        

    def _setValue(self, x, y, status, field):
        '''
        PRIVATE. Sets 'field' at (x, y) to 'status'. You should use one of the intermediate functions to accomplish a task using this function.
        @param x The x coordinate.
        @param y The y coordinate.
        @param status If true, set field to true. If false, set field to false.
        @param field Which field of the location should be edited.
        @throw IndexError if either x or y falls out of bounds.
        @throw KeyError if status is not a bool.
        '''
        if x > self.x_size or x < 0:
            raise IndexError(f"The given x coordinate {x} is outside of the bounds of the x-axis (Maximum: {self.x_size-1}).")
        elif y > self.y_size or y < 0:
            raise IndexError(f"The given y coordinate {y} is outside of the bounds of the y-axis (Maximum: {self.y_size-1}).")
        elif type(status) != bool:
            raise KeyError(f"The given data type {type(status)} does not correspond to any accepted data types (bool)")
        else:
            self.field[x+(self.x_size*y)][field] = status

    #def helpBottom:
        #display
        #shows the current amount cols and rows, and interpret how to using the cheat mode.
        
