import tkinter as tk
import random

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

        self.canvas = tk.Canvas(master, width=CELL_SIZE * BOARD_SIZE, height=CELL_SIZE * BOARD_SIZE)
        self.canvas.pack()

        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ball_ids = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.score = 0
        self.game_over = False

        self.draw_board()
        self.generate_balls(3)

        self.canvas.bind("<Button-1>", self.handle_click)
        self.selected_ball = None

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x0, y0 = col * CELL_SIZE, row * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def generate_balls(self, num_balls):
        empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if self.board[row][col] is None]
        random.shuffle(empty_cells)
        for _ in range(num_balls):
            if empty_cells:
                row, col = empty_cells.pop()
                color = random.choice(BALL_COLORS)
                self.board[row][col] = color
                self.draw_ball(row, col, color)

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

    def check_game_over(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is None:
                    return
        self.game_over = True
        self.master.title("Color Lines - Game Over!")


def main():
    root = tk.Tk()
    game = ColorLinesGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
