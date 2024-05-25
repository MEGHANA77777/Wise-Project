# Added grid choosing options
# Added more colors
# Changed background color
# Added background image
# Made the grid lines smoother
# Added music
# Mute/unmute button

import tkinter as tk
import random
from tkinter import messagebox
import pygame  # Import pygame for music functionality

# Initializing pygame mixer
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3') 
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Constants
BALL_COLORS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan"]
BALL_RADIUS = 20
CELL_SIZE = 50
MOVE_DELAY = 500  # in milliseconds
BACKGROUND_COLOR = "#333333"  # Dark grey background for a 3D spatial effect
CHECKBOX_COLOR = "#cccccc"  # Light grey color for checkboxes
FONT_STYLE = ("Helvetica", 14)  # Font style for labels and buttons

class ColorLinesGame:
    def __init__(self, master, grid_size):
        self.master = master
        self.grid_size = grid_size
        self.master.title(f"Color Lines - Score: 0")
        self.master.configure(bg=BACKGROUND_COLOR)

        self.frame = tk.Frame(master, bg=BACKGROUND_COLOR)
        self.frame.pack()

        self.next_canvas = tk.Canvas(self.frame, width=CELL_SIZE * 3, height=CELL_SIZE, bg='white', highlightthickness=0)
        self.next_canvas.pack(pady=10)
        self.next_canvas.create_text(75, 10, text="Next Balls", font=FONT_STYLE)

        self.canvas = tk.Canvas(self.frame, width=CELL_SIZE * self.grid_size, height=CELL_SIZE * self.grid_size, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.score_label = tk.Label(self.frame, text="Score: 0", font=FONT_STYLE, bg=BACKGROUND_COLOR, fg="white")
        self.score_label.pack(pady=10)

        self.mute_button = tk.Button(self.frame, text="Mute", font=FONT_STYLE, bg="gray", fg="white", command=self.toggle_music)
        self.mute_button.pack(pady=10)

        self.board = [[None] * self.grid_size for _ in range(self.grid_size)]
        self.ball_ids = [[None] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.music_muted = False

        self.next_balls = [None, None, None]
        self.background_image = PhotoImage(file='https://images.app.goo.gl/yw79kSgNY1UbwbzJ8')  # Load your background image
        self.canvas.create_image(100, 100, image=self.background_image, anchor="nw")  # Set the background image



        self.draw_board()
        self.generate_next_balls()
        self.generate_balls(3)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.selected_ball = None

    def draw_board(self):
        # Draw the board with a gradient effect for a smoother appearance
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x0, y0 = col * CELL_SIZE, row * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                gradient_color = '#%02x%02x%02x' % (255 - row * 5, 255 - row * 5, 255 - row * 5)  # Adjust color based on row for a 3D effect
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=3, fill=gradient_color)

    def generate_next_balls(self):
        # Generate the next set of balls to be displayed
        self.next_balls = [random.choice(BALL_COLORS) for _ in range(3)]
        self.display_next_balls()

    def display_next_balls(self):
        # Display the next set of balls on the next canvas
        self.next_canvas.delete("ball")
        for i, color in enumerate(self.next_balls):
            x, y = i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2 + 10
            self.next_canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color, tags="ball")

    def generate_balls(self, num_balls):
        # Generate new balls on the board
        empty_cells = [(row, col) for row in range(self.grid_size) for col in range(self.grid_size) if self.board[row][col] is None]
        random.shuffle(empty_cells)
        for i in range(num_balls):
            if empty_cells:
                row, col = empty_cells.pop()
                color = self.next_balls[i]
                self.board[row][col] = color
                self.draw_ball(row, col, color)
        self.generate_next_balls()

    def draw_ball(self, row, col, color):
        # Draw a ball on the canvas
        x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
        ball_id = self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color, tags=f"ball_{row}_{col}")
        self.ball_ids[row][col] = ball_id

    def handle_click(self, event):
        # Handle mouse click events for selecting and moving balls
        if self.game_over:
            return

        col, row = event.x // CELL_SIZE, event.y // CELL_SIZE

        if self.selected_ball:
            if self.board[row][col] is None:
                self.move_ball(self.selected_ball, (row, col))
                self.selected_ball = None
                self.generate_balls(3)
                self.check_lines()
                self.check_game_over()
            else:
                self.selected_ball = (row, col)
        else:
            if self.board[row][col] is not None:
                self.selected_ball = (row, col)

    def move_ball(self, from_pos, to_pos):
        # Move a ball from one position to another
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None

        self.canvas.move(self.ball_ids[from_row][from_col], (to_col - from_col) * CELL_SIZE, (to_row - from_row) * CELL_SIZE)
        self.ball_ids[to_row][to_col] = self.ball_ids[from_row][from_col]
        self.ball_ids[from_row][from_col] = None

    def check_lines(self):
        # Check for lines of five or more balls of the same color and remove them
        lines_removed = False
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board[row][col] is not None:
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        line = [(row, col)]
                        r, c = row, col
                        while 0 <= r + dr < self.grid_size and 0 <= c + dc < self.grid_size and self.board[r + dr][c + dc] == self.board[row][col]:
                            r += dr
                            c += dc
                            line.append((r, c))
                        if len(line) >= 5:
                            for r, c in line:
                                self.board[r][c] = None
                                self.canvas.delete(self.ball_ids[r][c])
                                self.ball_ids[r][c] = None
                            self.score += len(line) * 2
                            lines_removed = True

        if lines_removed:
            self.master.title("Color Lines - Score: " + str(self.score))
            self.score_label.config(text="Score: " + str(self.score))

    def check_game_over(self):
        # Check if the game is over (no empty cells left)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board[row][col] is None:
                    return
        self.game_over = True
        self.show_game_over_dialog()

    def show_game_over_dialog(self):
        # Show a dialog when the game is over
        response = messagebox.askyesnocancel("Game Over", f"Game Over! Your score is {self.score}.\nDo you want to play again?", icon="info")
        if response is None:
            self.master.destroy()  # User pressed Cancel (exit game)
        elif response:
            self.restart_game()  # User pressed Yes (restart game)
        else:
            self.go_to_home()  # User pressed No (go to home screen)

    def restart_game(self):
        # Restart the game
        self.canvas.delete("all")
        self.next_canvas.delete("all")
        self.__init__(self.master, self.grid_size)

    def go_to_home(self):
        # Go back to the home screen
        self.frame.destroy()
        HomeWindow(self.master)

    def toggle_music(self):
        # Mute/unmute the background music
        if self.music_muted:
            pygame.mixer.music.unpause()
            self.mute_button.config(text="Mute")
        else:
            pygame.mixer.music.pause()
            self.mute_button.config(text="Unmute")
        self.music_muted = not self.music_muted

class HomeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Lines")

        self.frame = tk.Frame(master, bg=BACKGROUND_COLOR)
        self.frame.pack
      
