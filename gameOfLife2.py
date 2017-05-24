## Have an alive list
import sys
class World:
    def __init__(self):
        self.aliveCells = {}
        self.deadCells = {}
        self.cellsToChange = {}
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0

    def makeCells(self, cellList):
        for cellKey in cellList:
            cells = cellKey.split(",") #slpit cellKey string into a list of strings
            newCell = Cell(int(cells[0]), int(cells[1]), self, True, 0)
            self.aliveCells[cellKey] = newCell

    def setBoundries(self, minX, maxX, minY, maxY):
        self.max_x = maxX
        self.min_x = minX
        self.max_y = maxY
        self.min_y = minY

    def step(self):
        for cellKey in self.aliveCells:
            self.aliveCells[cellKey].getNeighbors()
        for cellKey in self.cellsToChange:
            self.cellsToChange[cellKey].change(cellKey)
        self.cellsToChange = {}     #reset all but live cells dictionary to save space
        self.deadCells = {}
        self.printWorld()

    def printWorld(self):
        offset = 1
        for i in range(self.min_x - offset, self.max_x + offset):
            for j in range(self.min_y - offset, self.max_y + offset):
                nkey=str(i)+ ',' + str(j)
                if nkey in self.aliveCells:
                    print('X', end = ' ')
                else: print('*', end = ' ')
            print('',end='\n')
        print('-----------------------------------')



class Cell:
    def __init__(self, x, y, world = None, alive = False, aliveNeighborsCount=0):
        self.x = x
        self.y = y
        self.world = world
        self.alive = alive
        self.aliveNeighborsCount = aliveNeighborsCount

    def change(self, cellKey):
        if self.alive:
            self.alive = False
            del self.world.aliveCells[cellKey]
        else:
            self.alive = True
            self.world.aliveCells[cellKey] = self

    def getNeighbors(self):
        self.aliveNeighborsCount = 0    #reset neighbor counts for each new state
        for i in range(-1, 2):
            for j in range(-1,2):
                neighborX = self.x+i
                neighborY = self.y+j
                neighborKey = str(neighborX) + ',' +  str(neighborY)
                if neighborKey in self.world.aliveCells.keys() and str(i)+ ',' + str(j) != "0,0":
                    self.aliveNeighborsCount += 1
                else:
                    if neighborKey in self.world.deadCells.keys():
                        self.world.deadCells[neighborKey].aliveNeighborsCount += 1
                        if self.world.deadCells[neighborKey].aliveNeighborsCount == 3:
                            self.world.cellsToChange[neighborKey] = self.world.deadCells[neighborKey]
                        if self.world.deadCells[neighborKey].aliveNeighborsCount > 3:
                            del self.world.cellsToChange[neighborKey]
                    else:
                        self.world.deadCells[neighborKey] = Cell(neighborX, neighborY, self.world, False, 1)
        if self.aliveNeighborsCount < 2 or self.aliveNeighborsCount > 3:
            self.world.cellsToChange[str(self.x) + ',' + str(self.y)] = self



### MAIN
world = World()
world.makeCells(["0,0","0,1","0,2"])
world.setBoundries(-3, 3, -3, 3)
world.printWorld()
world.step()
world.step()
world.step()
world.step()