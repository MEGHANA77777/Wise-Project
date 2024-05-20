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
        self.master.title("Color Lines")

        self.canvas = tk.Canvas(master, width=CELL_SIZE * BOARD_SIZE, height=CELL_SIZE * BOARD_SIZE)
        self.canvas.pack()

        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.score = 0
        self.game_over = False

        self.draw_board()
        self.generate_balls(3)

        self.canvas.bind("<Button-1>", self.handle_click)

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
                x, y = col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=color)

    def handle_click(self, event):
        if self.game_over:
            return

        col, row = event.x // CELL_SIZE, event.y // CELL_SIZE
        if self.board[row][col] is None:
            print("Selected an empty cell!")
            return

        self.move_balls(row, col)

    def move_balls(self, row, col):
        selected_color = self.board[row][col]
        empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] is None]
        while empty_cells:
            new_row, new_col = random.choice(empty_cells)
            self.board[new_row][new_col] = selected_color
            x, y = new_col * CELL_SIZE + CELL_SIZE // 2, new_row * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_oval(x - BALL_RADIUS, y - BALL_RADIUS, x + BALL_RADIUS, y + BALL_RADIUS, fill=selected_color)
            empty_cells.remove((new_row, new_col))
            self.canvas.update_idletasks()

        self.check_lines()

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
                                self.canvas.delete("ball_" + str(r) + "_" + str(c))
                            self.score += len(line) * 2
                            lines_removed = True

        if lines_removed:
            self.master.title("Color Lines - Score: " + str(self.score))
            self.canvas.update_idletasks()
            self.canvas.after(MOVE_DELAY, self.shift_down)
        else:
            self.check_game_over()

    def shift_down(self):
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE - 1, -1, -1):
                if self.board[row][col] is None:
                    for r in range(row - 1, -1, -1):
                        if self.board[r][col] is not None:
                            self.board[row][col] = self.board[r][col]
                            self.board[r][col] = None
                            x0, y0 = col * CELL_SIZE, r * CELL_SIZE
                            x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                            self.canvas.move("ball_" + str(r) + "_" + str(col), 0, CELL_SIZE)
                            self.canvas.itemconfig("ball_" + str(r) + "_" + str(col), tags="ball_" + str(row) + "_" + str(col))
                            break
        self.canvas.update_idletasks()
        self.generate_balls(3)

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
