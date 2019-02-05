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
        if x > self.x_size:
            raise IndexError(f"The given x coordinate {x} is outside of the bounds of the x-axis (Maximum: {self.x_size-1}).")
        elif y > self.y_size:
            raise IndexError(f"The given y coordinate {y} is outside of the bounds of the y-axis (Maximum: {self.y_size-1}).")
        else:
            return self.field[x+(self.y_size*y)]
    
    def setFlagged(self, x, y, status):
        '''
        Sets the location at (x, y) to be either flagged or unflagged, dependent upon status.
        @param x The x coordinate.
        @param y The y coordinate.
        @param status If true, set flagged to true. If false, set flagged to false.
        '''
        self._setValue(x, y, status, 'flagged')
        
    def setBomb(self, x, y, status):
        '''
        Sets the location at (x, y) to be either have a bomb or not have a bomb, dependent upon status.
        @param x The x coordinate.
        @param y The y coordinate.
        @param status If true, set bomb to true. If false, set bomb to false.
        '''
        self._setValue(x, y, status, 'bomb')

    def setCleared(self, x, y, status):
        '''
        Sets the location at (x, y) to be either be cleared or not be cleared, dependent upon status.
        @param x The x coordinate.
        @param y The y coordinate.
        @param status If true, set cleared to true. If false, set cleared to false.
        '''
        self._setValue(x, y, status, 'cleared')


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
        if x > self.x_size:
            raise IndexError(f"The given x coordinate {x} is outside of the bounds of the x-axis (Maximum: {self.x_size-1}).")
        elif y > self.y_size:
            raise IndexError(f"The given y coordinate {y} is outside of the bounds of the y-axis (Maximum: {self.y_size-1}).")
        elif type(field) != bool:
            raise KeyError(f"The given data type {type(bool)} does not correspond to any accepted data types (bool)")
        else:
            self.field[x+(self.y_size*y)][field] = status