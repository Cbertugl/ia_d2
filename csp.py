import constants
import itertools

class CSP:
    # ================================================================================================
    # CONSTRUCTOR
    # ================================================================================================
    def __init__(self, sudoku):
        self.assignment = sudoku
        self.domain = constants.Domain
        self.variables = []
        self.constraints = []
        self.__generateVariablesAndConstraints()

    # ================================================================================================
    # PRIVATE FUNCTIONS
    # ================================================================================================
    def __generateVariablesAndConstraints(self):
        size = constants.GRID_SIZE

        # On crée une grille de variable temporaire pour les associer aux Tiles
        grid = self.assignment.getGrid()
        variableGrid = [[Variable(grid[j][i]) for i in range(size)] for j in range(size)]

        # On ajoute les variables au CSP
        for i in range(size):
            for j in range(size):
                self.variables.append(variableGrid[i][j])

        # On crée les contraintes sur chaque ligne
        for i in range(size):
            row = variableGrid[i]

            for j in range(size):
                variableOne = row[j]

                for k in range(j + 1, size):
                    variableTwo = row[k]
                    constraint = NotEqualConstraint(variableOne, variableTwo)
                    self.constraints.append(constraint)
                    variableOne.addConstraint(constraint)
                    variableTwo.addConstraint(constraint)

        # On crée les contraintes sur chaque colonne
        for i in range(size):
            column = []
            for row in variableGrid:
                column.append(row[i]) 

            for j in range(size):
                variableOne = column[j]

                for k in range(j + 1, size):
                    variableTwo = column[k]
                    constraint = NotEqualConstraint(variableOne, variableTwo)
                    self.constraints.append(constraint)
                    variableOne.addConstraint(constraint)
                    variableTwo.addConstraint(constraint)

        # On crée les contraintes dans chaque carré
        for squareI in range(3):
            for squareJ in range(3):
                square = []
                for i in range(3):
                    for j in range(3):
                        square.append(variableGrid[squareI * 3 + i][squareJ * 3 + j])
                    
                # On génère toutes les paires de case possible dans un carré
                squareList = list(itertools.product(square, square))

                # On enlève les paires avec deux cases sur la même ligne et/ou la même colonne
                # et les paires symétriques
                toRemove = []
                i = 0
                for p in squareList:
                    if(
                        p[0].object.getPosition()[0] == p[1].object.getPosition()[0] or
                        p[0].object.getPosition()[1] == p[1].object.getPosition()[1]
                    ):
                        toRemove.append(p)
                    else:
                        for q in range(i + 1, squareList.__len__()):
                            if(p[0].object.getPosition() == squareList[q][1].object.getPosition()): toRemove.append(squareList[q])

                    i += 1

                toRemove = set(toRemove)
                for p in toRemove:
                    squareList.remove(p)

                # On ajoute les contraintes restantes du carré
                for p in squareList:
                    variableOne = p[0]
                    variableTwo = p[1]
                    constraint = NotEqualConstraint(variableOne, variableTwo)
                    self.constraints.append(constraint)
                    variableOne.addConstraint(constraint)
                    variableTwo.addConstraint(constraint)

    def __isAssignementComplete(self):
        for v in self.variables:
            if(not v.isSet()): return False

        return True;

    def __getUnassignedVariable(self):
        # TODO: récupérer une variable non assignées avec le bon algo
        pass

    def __orderDomainValues(self, var):
        # TODO: implémenter least constraining value
        pass

    def __isConsistentWithValue(self, value):
        # TODO:
        pass

    # ================================================================================================
    # PUBLIC FUNCTIONS
    # ================================================================================================
    def displayVariables(self):
        for v in self.variables:
            v.displayConstraints()

    def backtrackingSearch(self):
        if(self.isAssignementComplete()): return self.assignment
        
        var = self.__getUnassignedVariable()
        for value in self.__orderDomainValues(var):
            if(self.__isConsistentWithValue(value)):
                var.setValue(value)

                result = self.backtrackingSearch()
                if(result != constants.FAILURE): return result
                var.removeValue()
        
        return constants.FAILURE


class Variable:
    def __init__(self, object):
        self.object = object
        self.constraints = []

    def isSet(self):
        return(self.getValue() != constants.NO_VALUE)

    def getValue(self):
        return self.object.getValue()

    def setValue(self, value):
        self.object.setValue(value)

    def removeValue(self):
        self.setValue(constants.NO_VALUE)

    def addConstraint(self, constraint):
        self.constraints.append(constraint)

    def getNbConstraints(self):
        return self.constraints.__len__()

    def displayConstraints(self):
        print("Case", self.object.getPosition(), end = "")
        if(self.isSet()) :print("; valeur", self.getValue(), end = "")
        print(";", self.getNbConstraints(), "contraintes")
        for c in self.constraints:
            if(c.variableOne == self): print(c.variableTwo.object.getPosition(), end = ", ")
            else : print(c.variableOne.object.getPosition(), end = ", ")
        print(end = "\n\n")


class NotEqualConstraint:
    def __init__(self, variableOne, variableTwo):
        self.variableOne = variableOne
        self.variableTwo = variableTwo

    def check(self):
        return(self.variableOne.getValue() != self.variableTwo.getValue())