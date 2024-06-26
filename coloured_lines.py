#With game over window play again and exit option only bg color
import tkinter as tk
import random
from tkinter import messagebox, PhotoImage
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Constants
BALL_COLORS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan"]
BALL_RADIUS = 20
CELL_SIZE = 50
MOVE_DELAY = 500
BACKGROUND_COLOR = "#FCF5C7"
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

        self.bg_image = tk.PhotoImage(file="bg4.png")  # Replace "background.png" with your image file
        self.bg_label = tk.Label(self.frame, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.next_canvas = tk.Canvas(self.frame, width=CELL_SIZE * 3, height=CELL_SIZE*1.2, bg="#FBCEB1", highlightthickness=0)
        self.next_canvas.pack(side="top", pady=10)
        self.next_canvas.create_text(75, 10, text="Next Balls", font=FONT_STYLE)

        self.canvas_frame = tk.Frame(self.frame, bg=BACKGROUND_COLOR)
        self.canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=CELL_SIZE * self.grid_size, height=CELL_SIZE * self.grid_size, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack()

        self.score_label = tk.Label(self.frame, text="Score: 0", font=("Showcard Gothic",28), bg="#FF964F", fg=TEXT_COLOR)
        self.score_label.place(relx=0.5, rely=0.87, anchor="center")

        self.back_button = tk.Button(self.frame, text="⌂", command=self.go_to_home, font=("Showcard Gothic", 23, "bold"),
                                     bg="#FF9AA2", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=10, pady=5)
        self.back_button.place(relx=0.01, rely=0.01, anchor="nw")

        self.restart_button = tk.Button(self.frame, text="RESTART", command=self.restart_game_window,
                                     font=("Showcard Gothic", 16, "bold"),
                                     bg="#C1CD97", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=8, pady=4)
        self.restart_button.place(relx=0.98, rely=0.02, anchor="ne")  # Top-right corner, slightly exceeding the frame

        self.exit_button = tk.Button(self.frame, text="EXIT", command=self.master.quit,
                                     font=("Showcard Gothic", 16, "bold"),
                                     bg="#FFA2A2", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=8, pady=4)
        self.exit_button.place(relx=0.98, rely=0.12, anchor="ne")  # Below the first button, with some space

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

        # Re-create the buttons
        self.next_canvas.create_text(75, 10, text="Next Balls", font=FONT_STYLE)
        
        self.back_button = tk.Button(self.frame, text="⌂", command=self.go_to_home,
                                     font=("Showcard Gothic", 23, "bold"),
                                     bg="#FF9AA2", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=10, pady=5)
        self.back_button.place(relx=0.01, rely=0.01, anchor="nw")

        self.score_label = tk.Label(self.frame, text="Score: 0", font=("Showcard Gothic", 28), bg="#FF964F",
                                    fg=TEXT_COLOR)
        self.score_label.place(relx=0.5, rely=0.87, anchor="center")

        self.restart_button = tk.Button(self.frame, text="RESTART", command=self.restart_game_window,
                                        font=("Showcard Gothic", 16, "bold"),
                                        bg="#C1CD97", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=8, pady=4)
        self.restart_button.place(relx=0.98, rely=0.02, anchor="ne")

        self.exit_button = tk.Button(self.frame, text="EXIT", command=self.master.quit,
                                     font=("Showcard Gothic", 16, "bold"),
                                     bg="#FFA2A2", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=8, pady=4)
        self.exit_button.place(relx=0.98, rely=0.12, anchor="ne")

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
        balls_to_generate = 3
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board[row][col] is not None:
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        line = [(row, col)]
                        r, c = row, col
                        while 0 <= r + dr < self.grid_size and 0 <= c + dc < self.grid_size and self.board[r + dr][
                            c + dc] == self.board[row][col]:
                            r += dr
                            c += dc
                            line.append((r, c))
                        if len(line) >= 5:
                            for r, c in line:
                                self.board[r][c] = None
                                self.canvas.delete(self.ball_ids[r][c])
                                self.ball_ids[r][c] = None
                            self.score += len(line) * 2
                            balls_to_generate = 0  # Set balls_to_generate to 0 when a line is removed
                            lines_removed = True

        if lines_removed:
            self.master.title(f"Color Lines - Score: {self.score}")
            self.score_label.config(text=f"Score: {self.score}")

        self.generate_balls(balls_to_generate)
    def check_game_over(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board[row][col] is None:
                    return
        self.game_over = True
        self.show_game_over_dialog()

    def show_game_over_dialog(self):
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title("Game Over")
        game_over_window.configure(bg=BACKGROUND_COLOR)

        # Set the screen size and center the window
        screen_width = 400
        screen_height = 200
        x = (game_over_window.winfo_screenwidth() // 2) - (screen_width // 2)
        y = (game_over_window.winfo_screenheight() // 2) - (screen_height // 2)
        game_over_window.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        game_over_label = tk.Label(game_over_window, text=f"Game Over!\nYour score is {self.score}", font=FONT_STYLE,
                                   fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        game_over_label.pack(pady=20)

        button_frame = tk.Frame(game_over_window, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        play_again_button = tk.Button(button_frame, text="Play Again",
                                      command=lambda: self.restart_game(game_over_window), font=FONT_STYLE,
                                      bg="#6EB5FF", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=20,
                                      pady=10)
        play_again_button.pack(side="left", padx=10)

        exit_button = tk.Button(button_frame, text="Exit", command=self.master.quit, font=FONT_STYLE, bg="#FE4F5F",
                                fg="#000000", padx=20, pady=10)
        exit_button.pack(side="right", padx=10)

    def restart_game_window(self):

        # Destroy the current game board
        self.canvas.delete("all")
        self.next_canvas.delete("all")
        self.score_label.destroy()
        self.back_button.destroy()
        self.restart_button.destroy()
        self.exit_button.destroy()

        # Re-initialize the game
        self.initialize_game()


    def restart_game(self, game_over_window):
        game_over_window.destroy()
        self.canvas.delete("all")
        self.next_canvas.delete("all")
        self.score_label.destroy()
        self.back_button.destroy()
        self.restart_button.destroy()
        self.exit_button.destroy()
        self.initialize_game()

    def go_to_home(self):
        self.frame.destroy()
        pygame.mixer.music.stop()  # Stop the music
        HomeWindow(self.master)

class HomeWindow:
    # ... (no changes in the HomeWindow class)
    def __init__(self, master):
        self.master = master
        self.master.title("Color Lines")

        # Set the screen size and center the window
        screen_width = 1300
        screen_height = 800
        x = (self.master.winfo_screenwidth() // 2) - (screen_width // 2)
        y = (self.master.winfo_screenheight() // 2) - (screen_height // 2)
        self.master.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        # Load and set the background image
        self.bg_image = tk.PhotoImage(file="bg1.png")
        self.bg_label = tk.Label(master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(master, text="Welcome to Color Lines!", font=("Jokerman", 36, "bold"), fg=TEXT_COLOR, bg="#FFF5BA" )
        self.label.place(relx=0.5, rely=0.2, anchor="center")

        self.grid_size_var = tk.IntVar(value=9)

        self.grid_size_label = tk.Label(master, text="Select Grid Size:", font=("Showcard Gothic", 24), fg=TEXT_COLOR, bg = "#FFF5BA")
        self.grid_size_label.place(relx=0.5, rely=0.35, anchor="center")

        self.grid_size_9 = tk.Radiobutton(master, text="9x9", variable=self.grid_size_var, value=9, font=("Showcard Gothic", 16), fg=TEXT_COLOR, selectcolor=BUTTON_HIGHLIGHT)
        self.grid_size_9.place(relx=0.5, rely=0.45, anchor="center")

        self.grid_size_10 = tk.Radiobutton(master, text="10x10", variable=self.grid_size_var, value=10, font=("Showcard Gothic", 16), fg=TEXT_COLOR, selectcolor=BUTTON_HIGHLIGHT)
        self.grid_size_10.place(relx=0.5, rely=0.55, anchor="center")

        self.play_button = tk.Button(master, text="Play", command=self.start_game, font=FONT_STYLE, bg="#6EB5FF", fg=TEXT_COLOR, activebackground=BUTTON_HIGHLIGHT, padx=20, pady=10)
        self.play_button.place(relx=0.5, rely=0.65, anchor="center")

        self.instructions_button = tk.Button(master, text="Instructions", command=self.show_instructions, font=FONT_STYLE, bg="#FEED4F", fg="#000000", padx=20, pady=10)
        self.instructions_button.place(relx=0.5, rely=0.75, anchor="center")

        self.exit_button = tk.Button(master, text="Exit", command=self.master.quit, font=FONT_STYLE, bg="#FE4F5F", fg="#000000", padx=20, pady=10)
        self.exit_button.place(relx=0.5, rely=0.85, anchor="center")

        self.play_music_button = tk.Button(master, text="Play Music", command=self.play_background_music,
                                          font=FONT_STYLE, bg="#ACE7FF", fg=TEXT_COLOR,
                                          activebackground=BUTTON_HIGHLIGHT, padx=20, pady=10)
        self.play_music_button.place(relx=0.1, rely=0.9, anchor="sw")

        self.stop_music_button = tk.Button(master, text="Stop Music", command=self.stop_background_music,
                                           font=FONT_STYLE, bg="#ACE7FF", fg=TEXT_COLOR,
                                           activebackground=BUTTON_HIGHLIGHT, padx=20, pady=10)
        self.stop_music_button.place(relx=0.9, rely=0.9, anchor="se")

        self.music_playing = False

    def start_game(self):
        grid_size = self.grid_size_var.get()
        ColorLinesGame(self.master, grid_size)

    def show_instructions(self):
        self.instruction_window = tk.Toplevel(self.master)
        self.instruction_window.title("Instructions")

        # Set the screen size and center the window
        screen_width = 900
        screen_height = 600
        x = (self.instruction_window.winfo_screenwidth() // 2) - (screen_width // 2)
        y = (self.instruction_window.winfo_screenheight() // 2) - (screen_height // 2)
        self.instruction_window.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        # Load and set the background image for the instruction window
        self.instruction_bg_image = tk.PhotoImage(file="bg.png")
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
        instructions_label = tk.Label(self.instruction_window, text=instructions_text, font=("Showcard Gothic", 14), fg=TEXT_COLOR, bg="#FFF5E1",wraplength=469, justify="left")
        instructions_label.place(relx=0.5, rely=0.499, anchor="center")

    def play_background_music(self):
        if not self.music_playing:
            pygame.mixer.music.load("background_music.mp3")  # Load your background music
            pygame.mixer.music.play(-1)  # Play the music in a loop
            self.music_playing = True

    def stop_background_music(self):
        if  self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False


if __name__ == "__main__":
    root = tk.Tk()
    root.iconphoto(True, PhotoImage(file="icon.png"))
    HomeWindow(root)
    root.mainloop()
    pygame.mixer.music.stop()  # Stop the music when the mainloop ends
