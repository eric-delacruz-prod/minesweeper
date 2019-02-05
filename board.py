#Minesweeper Board

class Board():
    all_tiles = []
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
        