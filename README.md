# minesweeper
A Minesweeper Project for EECS 448

## Running
Type the following command into the command line in the directory in which the project was cloned (assuming python and pygame are installed):

For Linux and Mac:
"python3 minesweeper.py"

For Windows:
"py minesweeper.py"

If pygame is not installed, (if the error 'ImportError: No module named pygame' appears) refer to this page for instructions: https://www.pygame.org/wiki/GettingStarted

You can change the size of the board and the number of bombs by adding additional arguments, like so:

"python3 minesweeper.py [number of bombs] [size along one side]" for a square field
or "python3 minesweeper.py [number of bombs] [width] [height]" for a rectangular field

## Rules and controls of the game

Your objective is to flag all the bombs on your board.
You can click on any square to reveal a bomb or number.
If a bomb is revealed you lose the game.
If a number is revealed the number indicates how many possible bombs there are around that square.
You must flag all bombs to win the game.
Left mouse button will reveal the current square you are hovering.
Right mouse button will place/remove a flag on the current square.
Middle mouse button/'c' will toggle a cheat mode to reveal all bombs without ending the game.
Good luck!


## Documentation

Documentation can be accessed by navigating to the HTML folder, and clicking index.html

## Contributors

Board Class: Owen Mellema (architectdrone)

Game Logic: Zach Fruend

GUI: Zach Davis

Tests: Guanyu Li, Aris Vinsant, and Gwen Liu

Group 2 Modifications: Kevin Dinh, Eric Seals, Fan, Eric Delacruz, Evan Trout

