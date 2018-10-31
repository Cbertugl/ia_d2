import constants
import csp
import sudoku


# ==================================================================================================
# MAIN
# ==================================================================================================
S = sudoku.Sudoku.getSudokuFromFile("sudoku/1.txt")
S.display()

CSP = csp.CSP(S)

CSP.displayVariables()