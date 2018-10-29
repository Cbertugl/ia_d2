import constants

class Sudoku:
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self):
        size = constants.GRID_SIZE
        self.grid = [[Tile(j+1,i+1) for i in range(size)] for j in range(size)]
        for i in range(size): 
            for j in range(size):
                neighbors = []
                if i > 0:
                    neighbors.append(self.grid[i-1][j])
                if i < size-1:
                    neighbors.append(self.grid[i+1][j])
                if j > 0:
                    neighbors.append(self.grid[i][j-1])
                if j < size-1:
                    neighbors.append(self.grid[i][j+1])   
                self.grid[i][j].setNeighbors(neighbors)
                
    # ==============================================================================================
    # GETTERS AND SETTERS
    # ==============================================================================================
    def getTile(self, line, row):
        return self.grid[line - 1][row - 1]

    def getGrid(self):
        return self.grid
    
    def setTileValue(self, line, row, value):
        self.grid[line -1 ][row - 1].setValue(value)
        
    def display(self):
        size = constants.GRID_SIZE
        line = "-"
        for j in range(size):
            line += "----"
        print(line) 
        for i in range(size):
            line = "|"
            for j in range(size):
                if(self.grid[i][j].getValue() == constants.DOMAIN[0]): line += "   |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[1]): line += " 1 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[2]): line += " 2 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[3]): line += " 3 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[4]): line += " 4 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[5]): line += " 5 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[6]): line += " 6 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[7]): line += " 7 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[8]): line += " 8 |"
                elif(self.grid[i][j].getValue() == constants.DOMAIN[9]): line += " 9 |"
            print(line)
            line = "-"
            for j in range(size):
                line += "----"
            print(line)    
        print("")

        
class Tile:
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self, line, row):
        self.line = line
        self.row = row
        self.neighbors = []
        self.value = constants.DOMAIN[0]
        
    # ==============================================================================================
    # GETTERS AND SETTERS
    # ============================================================================================== 
    def setNeighbors(self,neighbors):
        for i in range(len(neighbors)):
            self.neighbors.append(neighbors[i])
        
    def getPosition(self):
        return (self.line, self.row)
        
    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value =  constants.DOMAIN[value]
