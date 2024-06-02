# Color Lines Game - README

## Introduction
Color Lines is a puzzle game where the objective is to align at least five balls of the same color in a row either horizontally, vertically, or diagonally. This implementation of Color Lines uses Python's Tkinter library for the graphical user interface.

## Features
- Dynamic board with configurable grid size (9x9 or 10x10).
- Random generation of colored balls.
- Visual feedback on selected balls.
- Pathfinding to ensure valid moves.
- Scoring system based on the number of balls removed.

## Installation
Ensure you have Python installed. This game requires no additional packages other than Tkinter, which is included with Python standard library.

## How to Run
1. Save the code in a file named `color_lines.py`.
2. Open a terminal and navigate to the directory containing `color_lines.py`.
3. Run the script using:
   ```sh
   python color_lines.py
   ```

## Gameplay
1. Start the game and choose the grid size from the home screen.
2. Click on a ball to select it. Click on an empty cell to move the selected ball if a valid path exists.
3. Align five or more balls of the same color in a row to score points and remove the balls from the board.
4. The game ends when the board is full and no more moves are possible.
5. A dialog box will appear at the game over, offering options to restart or exit the game.

## Controls
- **Left Click**: Select a ball or move a selected ball to an empty cell.

## Code Structure
- Game Over Window- provides option to replay and exit
- `ColorLinesGame` class: Handles game logic, UI setup, and interactions.
- `HomeWindow` class: Provides the home screen for grid size selection.
- Main function: Initializes the game.

## Customization
- **BALL_COLORS**: Modify the list of colors to change ball appearances.
- **GRID_SIZE**: Adjust the default grid size by changing the `grid_size_var` in the `HomeWindow` class.

## Future Improvements
- Enhanced pathfinding for more efficient ball movements.
- Additional game modes and difficulty levels.
- Improved visual effects and animations.

## License
This project is not up for an open source project yet.

## Contact
For issues or contributions, please comment.

---

Enjoy the game!
