import random
from collections import deque

# Game variables
grid = []
forecast = []
score = 0
record = 0
selected = None
blocked = False

# Game DOM elements
gridElement = None
forecastElement = None
scoreElement = None
recordElement = None

# Ball colors
colors = {
    1: 'blue',
    2: 'cyan',
    3: 'red',
    4: 'brown',
    5: 'green',
    6: 'yellow',
    7: 'magenta',
    'key': lambda color: next(key for key, value in colors.items() if value == color)
}

def init():
    """
    Initializes the game
    """
    global gridElement, forecastElement, scoreElement, recordElement, grid, score, blocked, selected, record

    # Gets game DOM elements
    gridElement = document.querySelector('.grid')
    forecastElement = document.querySelector('.forecast')
    scoreElement = document.querySelector('.score')
    recordElement = document.querySelector('.record')

    # Sets default game values
    grid = [[0 for _ in range(9)] for _ in range(9)]
    score = 0
    blocked = False
    selected = None

    # Tries to get the record from the local storage
    record = int(localStorage.getItem('lines-record') or 0)

    # Generates forecast balls
    forecastBalls()

    # Creates grid
    createGrid()

    scoreElement.innerHTML = str(score)
    recordElement.innerHTML = str(record)

def createGrid():
    """
    Creates the grid
    """
    global grid, gridElement

    # Clears grid element
    gridElement.innerHTML = ''

    for i in range(9):
        grid[i] = [0] * 9
        for j in range(9):
            # Creates new cell
            cell = document.createElement('div')

            # Sets cell attributes
            cell.id = f'cell-{j}-{i}'
            cell.className = 'empty'
            cell.dataset.x = str(j)
            cell.dataset.y = str(i)
            cell.style.left = f'{j * 50}px'
            cell.style.top = f'{i * 50}px'

            # Adds cell to the grid
            gridElement.appendChild(cell)

            # Listens for a click event
            cell.addEventListener('click', lambda e: onCellClick(e), False)

    # Adds random balls on the grid
    addBalls()

def getCells(selector):
    """
    Gets cells by selector
    """
    return gridElement.querySelectorAll(selector)

def getCell(x, y):
    """
    Gets specific cell by x and y coordinates
    """
    return document.getElementById(f'cell-{x}-{y}')

def onCellClick(e):
    """
    Event: cell clicked
    """
    global selected, blocked

    if blocked:
        return
    elif e.currentTarget.className == 'empty':
        onEmptyCellClick(e)
    else:
        onBallClick(e)

def onBallClick(e):
    """
    Event: ball clicked
    """
    global selected

    # Unselects previously selected cell
    for cell in getCells('.ball'):
        if cell.classList.contains('selected'):
            cell.classList.remove('selected')
            break

    # Marks clicked cell as selected
    e.currentTarget.classList.add('selected')
    selected = e.currentTarget

def onEmptyCellClick(e):
    """
    Event: empty cell clicked
    """
    global selected

    # Checks if any cell is selected
    if not selected:
        return

    to = e.currentTarget
    from_ = selected

    # Tries to find the path
    astar = Astar(grid)
    path = astar.find(int(from_.dataset.x), int(from_.dataset.y), int(to.dataset.x), int(to.dataset.y))

    # Checks if path were found
    if path:
        moveBall(from_, to, path, lambda: handleLines(to))
    else:
        # TODO: Handle the case when no path is found
        pass

def forecastBalls():
    """
    Generates forecast balls
    """
    global forecast, forecastElement

    forecast = [random.randint(1, 7) for _ in range(3)]
    forecastElement.innerHTML = ''.join(f'<div class="ball" style="background-color: {colors[ball]}"></div>' for ball in forecast)

def addBalls(callback=None):
    """
    Adds random balls on the grid
    """
    global grid, gridElement

    cells = [cell for cell in getCells('.empty')]
    if cells:
        for _ in range(random.randint(1, 3)):
            cell = random.choice(cells)
            cell.className = 'ball'
            cell.style.backgroundColor = colors[random.randint(1, 7)]
            grid[int(cell.dataset.y)][int(cell.dataset.x)] = colors.key(cell.style.backgroundColor)
            cells.remove(cell)
        if callback:
            callback(cells)

def moveBall(from_, to, path, callback):
    """
    Moves a ball from one cell to another
    """
    global grid, selected

    # Move the ball
    to.className = 'ball'
    to.style.backgroundColor = from_.style.backgroundColor
    grid[int(to.dataset.y)][int(to.dataset.x)] = grid[int(from_.dataset.y)][int(from_.dataset.x)]
    from_.className = 'empty'
    grid[int(from_.dataset.y)][int(from_.dataset.x)] = 0
    selected = None

    # Call the callback function
    callback()

def getLines(cell):
    """
    Gets five-ball lines for a given cell
    """
    global grid

    x, y = int(cell.dataset.x), int(cell.dataset.y)
    color = grid[y][x]

    # Check horizontal lines
    for dx in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
        if 0 <= x + dx < 9 and grid[y][x + dx] == color:
            line = [(x + i, y) for i in range(dx, dx + 5)]
            if all(grid[y][x + i] == color for i in range(dx, dx + 5)):
                return line

    # Check vertical lines
    for dy in [-4, -3, -2, -1, 0, 1, 2, 3, 4]:
        if 0 <= y + dy < 9 and grid[y + dy][x] == color:
            line = [(x, y + i) for i in range(dy, dy + 5)]
            if all(grid[y + i][x] == color for i in range(dy, dy + 5)):
                return line

    return None

def removeLines(lineSets):
    """
    Removes five-ball lines from the grid
    """
    global grid, score, record, blocked

    for lines in lineSets:
        for x, y in lines:
            grid[y][x] = 0
            getCell(x, y).className = 'empty'
        score += 100 * len(lines)
        scoreElement.innerHTML = str(score)

        if score > record:
            record = score
            recordElement.innerHTML = str(record)
            localStorage.setItem('lines-record', str(record))

    blocked = True
    addBalls(lambda cells: handleLines(cells[0]))

def handleLines(cell):
    """
    Handles the lines after a ball is moved
    """
    global blocked

    lines = getLines(cell)
    if lines:
        removeLines([lines])
    else:
        addBalls(lambda cells: handleLines(cells[0]))
    blocked = False

class Astar:
    """
    A* pathfinding algorithm
    """
    def __init__(self, grid):
        self.grid = grid

    def find(self, start_x, start_y, end_x, end_y):
        """
        Finds the path from the start to the end cell
        """
        start = (start_x, start_y)
        end = (end_x, end_y)

        open_set = deque([(0, start)])
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_set:
            current = open_set.popleft()[1]

            if current == end:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
                    open_set.append((f_score[neighbor], neighbor))

        return None

    def get_neighbors(self, cell):
        """
        Gets the neighboring cells of a given cell
        """
        x, y = cell
        neighbors = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 9 and 0 <= ny < 9 and self.grid[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors

    def heuristic(self, a, b):
        """
        Calculates the Manhattan distance between two cells
        """
        (x1, y1), (x2, y2) = a, b
        return abs(x1 - x2) + abs(y1 - y2)

    def reconstruct_path(self, came_from, current):
        """
        Reconstructs the path from the start to the end cell
        """
        path = [(int(current[0]), int(current[1]))]
        while current in came_from:
            current = came_from[current]
            path.append((int(current[0]), int(current[1])))
        path.reverse()
        return path


    
