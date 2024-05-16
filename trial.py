import random, math

class Lines:
    def __init__(self):
        self.grid = []
        self.forecast = []
        self.score = 0
        self.record = 0
        self.selected = None
        self.blocked = False
        self.gridElement = None
        self.forecastElement = None
        self.scoreElement = None
        self.recordElement = None
        self.colors = {
            1: 'blue',
            2: 'cyan',
            3: 'red',
            4: 'brown',
            5: 'green',
            6: 'yellow',
            7: 'magenta'
        }

    def init(self):
        self.gridElement = None
        self.forecastElement = None
        self.scoreElement = None
        self.recordElement = None
        self.grid = []
        self.score = 0
        self.blocked = False
        self.selected = None
        self.record = 0
        self.record = 0
        self.forecastBalls()
        self.createGrid()
        self.scoreElement.innerHTML = self.score
        self.recordElement.innerHTML = self.record

    def createGrid(self):
        self.gridElement.innerHTML = ''
        for i in range(9):
            self.grid[i] = []
            for j in range(9):
                self.grid[i][j] = 0
                cell = document.createElement('div')
                cell.id = 'cell-'+j+'-'+i
                cell.className = 'empty'
                cell.dataset.x = j
                cell.dataset.y = i
                cell.style.left = (j*50)+'px'
                cell.style.top = (i*50)+'px'
                self.gridElement.appendChild(cell)
                cell.addEventListener('click', self.onEmptyCellClick, False)
        self.addBalls()

    def getCells(self, selector):
        return self.gridElement.querySelectorAll(selector)

    def getCell(self, x, y):
        return document.getElementById('cell-'+x+'-'+y)

    def onBallClick(self, e):
        for cell in self.getCells('.ball'):
            if cell.classList.contains('selected'):
                cell.classList.remove('selected')
                break
        e.currentTarget.classList.add('selected')
        self.selected = e.currentTarget

    def onEmptyCellClick(self, e):
        if not self.selected:
            return
        to = e.currentTarget
        from_ = self.selected
        astar = self.Astar(self.grid)
        path = astar.find(from_.dataset.x, from_.dataset.y, to.dataset.x, to.dataset.y)
        if path:
            self.moveBall(from_, to, path, self.afterMoveBall)

    def addBalls(self, callback=None):
        self.blocked = True
        cells = []
        for i in range(3):
            emptyCells = self.getCells('.empty')
            if len(emptyCells) > 0:
                cell = emptyCells[random.randint(0, len(emptyCells)-1)]
                self.grid[cell.dataset.y][cell.dataset.x] = self.colors.key(self.forecast[i])
                cells.append(cell)
                cell.className = 'ball '+self.forecast[i]+' fadein'
            else:
                break
        setTimeout(lambda: self.fadeInBalls(cells, callback), 300)
        self.forecastBalls()

    def fadeInBalls(self, cells, callback):
        for cell in self.getCells('.fadein'):
            cell.classList.remove('fadein')
        self.blocked = False
        if callback:
            callback(cells)

    def removeLines(self, lineSets):
        self.blocked = True
        for lines in lineSets:
            scoreAdd = 0
            for line in lines:
                for point in line:
                    x = point[0]
                    y = point[1]
                    cell = self.getCell(x, y)
                    cell.classList.add('fadeout')
                    self.grid[y][x] = 0
                    scoreAdd += 2
        self.updateScore(scoreAdd)
        setTimeout(self.fadeOutLines, 300)

    def fadeOutLines(self):
        for cell in self.getCells('.fadeout'):
            cell.className = 'empty'
        self.blocked = False

    def moveBall(self, from_, to, path, callback):
        self.blocked = True
        self.grid[from_.dataset.y][from_.dataset.x] = 0
        color = from_.classList.item(1)
        previous = None
        from_.className = 'empty'
        self.selected = None
        for i in range(len(path)+1):
            if i == len(path):
                self.grid[to.dataset.y][to.dataset.x] = self.colors.key(color)
                to.className = 'ball '+color
                self.blocked = False
                callback()
            else:
                if previous:
                    previous.className = 'empty'
                cell = previous = self.getCell(path[i].x, path[i].y)
                cell.className = 'ball '+color

    def getLines(self, cell):
        x = int(cell.dataset.x)
        y = int(cell.dataset.y)
        ball = self.colors.key(cell.classList.item(1))
        lines = [[[x,y]], [[x,y]], [[x,y]], [[x,y]]]
        l = r = d = u = lu = ru = ld = rd = ball
        i = 1
        while ball in [l,r,d,u,lu,ru,ld,rd]:
            if l == self.grid[y][x-i]:
                lines[0].append([x-i,y])
            else:
                l = -1
            if r == self.grid[y][x+i]:
                lines[0].append([x+i,y])
            else:
                r = -1
            if y-i >= 0 and u == self.grid[y-i][x]:
                lines[1].append([x,y-i])
            else:
                u = -1
            if y+i <= 8 and d == self.grid[y+i][x]:
                lines[1].append([x,y+i])
            else:
                d = -1
            if y-i >= 0 and lu == self.grid[y-i][x-i]:
                lines[2].append([x-i,y-i])
            else:
                lu = -1
            if y+i <= 8 and rd == self.grid[y+i][x+i]:
                lines[2].append([x+i,y+i])
            else:
                rd = -1
            if y+i <= 8 and ld == self.grid[y+i][x-i]:
                lines[3].append([x-i,y+i])
            else:
                ld = -1
            if y-i >= 0 and ru == self.grid[y-i][x+i]:
                lines[3].append([x+i,y-i])
            else:
                ru = -1
            i += 1
        for i in range(len(lines)-1, -1, -1):
            if len(lines[i]) < 5:
                lines.pop(i)
        return lines if len(lines) > 0 else False

    def forecastBalls(self):
        self.forecast = []
        self.forecastElement.innerHTML = ''
        for i in range(3):
            ball = document.createElement('div')
            self.forecast[i] = self.colors[random.randint(1, 7)]
            ball.className = 'ball '+self.forecast[i]
            self.forecastElement.appendChild(ball)

    def updateScore(self, add):
        self.score += add
        if self.score > self.record:
            localStorage.setItem('lines-record', self.score)
            self.recordElement.innerHTML = self.record = self.score
        self.scoreElement.innerHTML = self.score

    def gameOver(self):
        self.blocked = True
        if confirm('Game over! Your score is '+self.score+'!\nPlay again?'):
            self.init()

    def rand(self, from_, to):
        return (math.floor(math.random() * (to-(from_+1)) + from_))

    def each(self, object, callback):
        for i in range(len(object)):
            callback(object[i], i)

    class Astar:
        def __init__(self, grid):
            self.nodes = []
            self.openset = []

        def init(self, startX, startY):
            for i in range(9):
                self.nodes[i] = []
                for j in range(9):
                    self.nodes[i][j] = {
                        'obstacle': self.grid[i][j],
                        'parent': 0,
                        'f': 0,
                        'g': 0,
                        'h': 0,
                        'x': j,
                        'y': i,
                        'closed': False
                    }
            self.openset.append(self.nodes[startY][startX])

        def find(self, startX, startY, endX, endY):
            self.init(startX, startY)
            while len(self.openset) > 0:
                index = 0
                for i in range(len(self.openset)):
                    if self.openset[i].f < self.openset[index].f:
                        index = i
                currentNode = self.openset[index]
                if currentNode.x == endX and currentNode.y == endY:
                    return self.reconstructPath(currentNode)
                self.openset.pop(index)
                currentNode.closed = True
                neighbors = self.getNeighbors(currentNode)
                for neighbor in neighbors:
                    if neighbor.closed or neighbor.obstacle != 0:
                        continue
                    g = currentNode.g+1
                    gIsBest = False
                    if not self.isOpened(neighbor):
                        gIsBest = True
                        neighbor.h = abs(neighbor.x-endX) + abs(neighbor.y-endY)
                        self.openset.append(neighbor)
                    elif g < neighbor.g:
                        gIsBest = True
                    if gIsBest:
                        neighbor.parent = currentNode
                        neighbor.g = g
                        neighbor.f = neighbor.g + neighbor.h
            return False

        def reconstructPath(self, node):
            path = []
            while node.parent:
                path.append(node)
                node = node.parent
            return path.reverse()

        def getNeighbors(self, node):
            neighbors = []
            x = node.x
            y = node.y
            if y-1 >= 0:
                neighbors.append(self.nodes[y-1][x])
            if y+1 <= 8:
                neighbors.append(self.nodes[y+1][x])
            if x-1 >= 0:
                neighbors.append(self.nodes[y][x-1])
            if x+1 <= 8:
                neighbors.append(self.nodes[y][x+1])
            return neighbors

        def isOpened(self, node):
            for i in range(len(self.openset)):
                if self.openset[i].x == node.x and self.openset[i].y == node.y:
                    return True
            return False

    def __init__(self):
        self.init()
