import tkinter as tk
import random
from tkinter import messagebox
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Constants
BALL_COLORS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan"]
BALL_RADIUS = 20
CELL_SIZE = 50
MOVE_DELAY = 500
BACKGROUND_COLOR = "#B284BE"
BUTTON_COLOR = "#2980B9"
BUTTON_HIGHLIGHT = "#3498DB"
TEXT_COLOR = "#1B1B1B"
FONT_STYLE = ("Showcard Gothic", 14)

class ColorLinesGame:
    def __init__(self, master, grid_size):
        self.master = master
        self.grid_size = grid_size
        self.master.title(f"Color lines")
        self.master.configure(bg=BACKGROUND_COLOR)

        self.frame = tk.Frame(master, bg=BACKGROUND_COLOR)
        self.frame.pack(fill="both", expand=True)

        self.next_canvas = tk.Canvas(self.frame, width=CELL_SIZE * 3, height=CELL_SIZE*1.2, bg="#FBCEB1", highlightthickness=0)
        self.next_canvas.pack(side="top", pady=10)
        self.next_canvas.create_text(75, 10, text="Next Balls", font=FONT_STYLE)

        self.canvas_frame = tk.Frame(self.frame, bg=BACKGROUND_COLOR)
        self.canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=CELL_SIZE * self.grid_size, height=CELL_SIZE * self.grid_size, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(self.frame, text="Score: 0", font=FONT_STYLE, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.score_label.pack(side="bottom", pady=10)

        self.initialize_game()

    def initialize_game(self):
        self.board = [[None] * self.grid_size for _ in range(self.grid_size)]
        self.ball_ids = [[None] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False

        self.next_balls = [None, None, None]

        self.draw_board()
        self.generate_next_balls()
        self.generate_balls(3)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.selected_ball = None

    # ... (rest of the ColorLinesGame class remains the same)
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x0, y0 = col * CELL_SIZE, row * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                gradient_color = '#%02x%02x%02x' % (255 - row * 5, 255 - row * 5, 255 - row * 5)
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=3, fill=gradient_color)

    def generate_next_balls(self):
        self.next_balls = [random.choice(BALL_COLORS) for _ in range(3)]
        self.display_next_balls()

    def display_next_balls(self):
        self.next_canvas.delete("ball")
        for i, color in enumerate(self.next_balls):
            x, y = i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2 + 10
            self.next_canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS+6, x + BALL_RADIUS, y + BALL_RADIUS, fill=color, tags="ball")

    def generate_balls(self, num_balls):
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
        x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
        ball_id = self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color, tags=f"ball_{row}_{col}")
        self.ball_ids[row][col] = ball_id

    def handle_click(self, event):
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
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None

        self.canvas.move(self.ball_ids[from_row][from_col], (to_col - from_col) * CELL_SIZE, (to_row - from_row) * CELL_SIZE)
        self.ball_ids[to_row][to_col] = self.ball_ids[from_row][from_col]
        self.ball_ids[from_row][from_col] = None

    def check_lines(self):
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
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board[row][col] is None:
                    return
        self.game_over = True
        self.show_game_over_dialog()

    def show_game_over_dialog(self):
        response = messagebox.askyesnocancel("Game Over", f"Game Over! Your score is {self.score}.\nDo you want to play again?", icon="info")
        if response is None:
            self.master.destroy()
        elif response:
            self.restart_game()
        else:
            self.go_to_home()

    def restart_game(self):
        self.initialize_game()

    def go_to_home(self):
        self.frame.destroy()
        HomeWindow(self.master)


class HomeWindow:
    # ... (no changes in the HomeWindow class)
    def __init__(self, master):
        self.master = master
        self.master.title("Color Lines")

        # Set the screen size and center the window
        screen_width = 800
        screen_height = 600
        x = (self.master.winfo_screenwidth() // 2) - (screen_width // 2)
        y = (self.master.winfo_screenheight() // 2) - (screen_height // 2)
        self.master.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        # Load and set the background image
        self.bg_image = tk.PhotoImage(file="background.png")
        self.bg_label = tk.Label(master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(master, text="Welcome to Color Lines!", font=("Jokerman", 36, "bold"), fg=TEXT_COLOR)
        self.label.place(relx=0.5, rely=0.2, anchor="center")

        self.grid_size_var = tk.IntVar(value=9)

        self.grid_size_label = tk.Label(master, text="Select Grid Size:", font=("Showcard Gothic", 24), fg=TEXT_COLOR)
        self.grid_size_label.place(relx=0.5, rely=0.35, anchor="center")

        self.grid_size_9 = tk.Radiobutton(master, text="9x9", variable=self.grid_size_var, value=9, font=("Showcard Gothic", 16), fg=TEXT_COLOR, selectcolor=BUTTON_HIGHLIGHT)
        self.grid_size_9.place(relx=0.5, rely=0.45, anchor="center")

        self.grid_size_10 = tk.Radiobutton(master, text="10x10", variable=self.grid_size_var, value=10, font=("Showcard Gothic", 16), fg=TEXT_COLOR, selectcolor=BUTTON_HIGHLIGHT)
        self.grid_size_10.place(relx=0.5, rely=0.55, anchor="center")

        self.play_button = tk.Button(master, text="Play", command=self.start_game, font=FONT_STYLE, bg=BUTTON_COLOR, fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=20, pady=10)
        self.play_button.place(relx=0.5, rely=0.65, anchor="center")

        self.instructions_button = tk.Button(master, text="Instructions", command=self.show_instructions, font=FONT_STYLE, bg="#FFBF00", fg="#000000", padx=20, pady=10)
        self.instructions_button.place(relx=0.5, rely=0.75, anchor="center")

        self.exit_button = tk.Button(master, text="Exit", command=self.master.quit, font=FONT_STYLE, bg="red", fg="#000000", padx=20, pady=10)
        self.exit_button.place(relx=0.5, rely=0.85, anchor="center")

    def start_game(self):
        grid_size = self.grid_size_var.get()
        ColorLinesGame(self.master, grid_size)

    def show_instructions(self):
        self.instruction_window = tk.Toplevel(self.master)
        self.instruction_window.title("Instructions")

        # Set the screen size and center the window
        screen_width = 800
        screen_height = 600
        x = (self.instruction_window.winfo_screenwidth() // 2) - (screen_width // 2)
        y = (self.instruction_window.winfo_screenheight() // 2) - (screen_height // 2)
        self.instruction_window.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        # Load and set the background image for the instruction window
        self.instruction_bg_image = tk.PhotoImage(file="background.png")
        self.instruction_bg_label = tk.Label(self.instruction_window, image=self.instruction_bg_image)
        self.instruction_bg_label.place(relwidth=1, relheight=1)

        instructions_text = (
            "Welcome to Color Lines!\n\n"
            "The goal of the game is to score points by forming lines of at least five balls of the same color.\n\n"
            "How to play:\n"
            "1. Click on a ball to select it.\n"
            "2. Click on an empty cell to move the selected ball there.\n"
            "3. Form lines horizontally, vertically, or diagonally with at least five balls of the same color.\n"
            "4. Each time you move a ball, three new balls will appear on the board.\n\n"
            "The game ends when the board is full and there are no empty cells left.\n\n"
            "Good luck and have fun!"
        )
        instructions_label = tk.Label(self.instruction_window, text=instructions_text, font=("Showcard Gothic", 14), fg=TEXT_COLOR, wraplength=600, justify="left")
        instructions_label.place(relx=0.5, rely=0.5, anchor="center")


        def play_background_music(self):
            pygame.mixer.music.load("background_music.mp3")  # Load your background music
            pygame.mixer.music.play(-1)  # Play the music in a loop


if __name__ == "__main__":
    root = tk.Tk()
    HomeWindow(root)
    root.mainloop()
    pygame.mixer.music.stop()  # Stop the music when the mainloop ends
