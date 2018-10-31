import constants

class CSP:
  # ================================================================================================
  # CONSTRUCTOR
  # ================================================================================================
  def __init__(self, sudoku):
    self.assignment = sudoku
    self.constraints = self.__generateConstraints()

  # ================================================================================================
  # PRIVATE FUNCTIONS
  # ================================================================================================
  def __generateConstraints(self):
    # TODO: générer les contraintes binaires
    pass
  
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
  # var est une Tile de Sudoku
  # value fait partie de constants.DOMAIN
  def backtrackingSearch(self):
    if(self.assignment.isComplete()): return self.assignment
    
    var = self.__getUnassignedVariable()
    for value in self.__orderDomainValues(var):
      if(self.__isConsistentWithValue(value)):
        var.setValue(value)

        result = self.backtrackingSearch()
        if(result != constants.FAILURE): return result
        var.removeValue()
    
    return constants.FAILURE


# class Constraint:
#   def __init__(self, sudoku):
#     self.