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
    # STATIC
    # ==============================================================================================
    @staticmethod
    def getSudokuFromFile(filename = "sudoku/1.txt"):
        file = open(filename, "r")
        sudoku = Sudoku()

        for i in range(9):
            line = file.readline()

            for j in range(9):
                if(line[j] == ''): sudoku.setTileValue(i + 1, j + 1, constants.NO_VALUE)
                if(line[j] == '1'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.ONE)
                if(line[j] == '2'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.TWO)
                if(line[j] == '3'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.THREE)
                if(line[j] == '4'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.FOUR)
                if(line[j] == '5'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.FIVE)
                if(line[j] == '6'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.SIX)
                if(line[j] == '7'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.SEVEN)
                if(line[j] == '8'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.EIGHT)
                if(line[j] == '9'): sudoku.setTileValue(i + 1, j + 1, constants.Domain.NINE)
        
        return sudoku

                
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
        line = "--"
        for j in range(size):
            line += "-----"
        print(line) 
        print(line)
        for i in range(size):
            line = "||"
            for j in range(size):
                if(self.grid[i][j].getValue() == constants.NO_VALUE): line += "   "
                elif(self.grid[i][j].getValue() == constants.Domain.ONE): line += " 1 "
                elif(self.grid[i][j].getValue() == constants.Domain.TWO): line += " 2 "
                elif(self.grid[i][j].getValue() == constants.Domain.THREE): line += " 3 "
                elif(self.grid[i][j].getValue() == constants.Domain.FOUR): line += " 4 "
                elif(self.grid[i][j].getValue() == constants.Domain.FIVE): line += " 5 "
                elif(self.grid[i][j].getValue() == constants.Domain.SIX): line += " 6 "
                elif(self.grid[i][j].getValue() == constants.Domain.SEVEN): line += " 7 "
                elif(self.grid[i][j].getValue() == constants.Domain.EIGHT): line += " 8 "
                elif(self.grid[i][j].getValue() == constants.Domain.NINE): line += " 9 "
                if (j+1)%3 == 0 : line += "||"
                else : line += " |"
            print(line)
            line = "--"
            for j in range(size):
                line += "-----"
            print(line)
            if (i+1)%3 == 0 : print(line)
        print("")


class Tile:
    # ==============================================================================================
    # CONSTRUCTOR
    # ==============================================================================================
    def __init__(self, line, row):
        self.line = line
        self.row = row
        self.neighbors = []
        self.value = constants.NO_VALUE
        
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
        self.value = value
