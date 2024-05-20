import tkinter as tk
import random
from tkinter import messagebox

# Constants
BOARD_SIZE = 9
BALL_COLORS = ["red", "blue", "green", "yellow", "orange"]
BALL_RADIUS = 20
CELL_SIZE = 50
MOVE_DELAY = 500  # in milliseconds

class ColorLinesGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Lines - Score: 0")

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.next_canvas = tk.Canvas(self.frame, width=CELL_SIZE * 3, height=CELL_SIZE, bg='white', highlightthickness=0)
        self.next_canvas.pack(pady=10)
        self.next_canvas.create_text(75, 10, text="Next Balls", font=("Helvetica", 12, "bold"))

        self.canvas = tk.Canvas(self.frame, width=CELL_SIZE * BOARD_SIZE, height=CELL_SIZE * BOARD_SIZE, bg='white', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.score_label = tk.Label(self.frame, text="Score: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ball_ids = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.score = 0
        self.game_over = False

        self.next_balls = [None, None, None]

        self.draw_board()
        self.generate_next_balls()
        self.generate_balls(3)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.selected_ball = None

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x0, y0 = col * CELL_SIZE, row * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=2)

    def generate_next_balls(self):
        self.next_balls = [random.choice(BALL_COLORS) for _ in range(3)]
        self.display_next_balls()

    def display_next_balls(self):
        self.next_canvas.delete("ball")
        for i, color in enumerate(self.next_balls):
            x, y = i * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE // 2 + 10
            self.next_canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color, tags="ball")

    def generate_balls(self, num_balls):
        empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if self.board[row][col] is None]
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
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is not None:
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        line = [(row, col)]
                        r, c = row, col
                        while 0 <= r + dr < BOARD_SIZE and 0 <= c + dc < BOARD_SIZE and self.board[r + dr][c + dc] == self.board[row][col]:
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
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is None:
                    return
        self.game_over = True
        self.show_game_over_dialog()

    def show_game_over_dialog(self):
        response = messagebox.askyesnocancel("Game Over", f"Game Over! Your score is {self.score}.\nDo you want to play again?", icon="info")
        if response is None:
            self.master.destroy()  # User pressed Cancel (exit game)
        elif response:
            self.restart_game()  # User pressed Yes (restart game)
        else:
            self.go_to_home()  # User pressed No (go to home screen)

    def restart_game(self):
        self.canvas.delete("all")
        self.next_canvas.delete("all")
        self.__init__(self.master)

    def go_to_home(self):
        self.frame.destroy()
        HomeWindow(self.master)

class HomeWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Lines")

        self.frame = tk.Frame(master, bg="lightblue")
        self.frame.pack(fill="both", expand=True)

        self.label = tk.Label(self.frame, text="Welcome to Color Lines!", font=("Helvetica", 24, "bold"), bg="lightblue")
        self.label.pack(pady=30)

        self.play_button = tk.Button(self.frame, text="Play", command=self.start_game, font=("Helvetica", 18), bg="green", fg="white", padx=20, pady=10)
        self.play_button.pack(pady=10)

        self.exit_button = tk.Button(self.frame, text="Exit", command=self.master.quit, font=("Helvetica", 18), bg="red", fg="white", padx=20, pady=10)
        self.exit_button.pack(pady=10)

    def start_game(self):
        self.frame.destroy()
        ColorLinesGame(self.master)

def main():
    root = tk.Tk()
    home_window = HomeWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
