class DFA:
  """Blah"""
  lexeme = ''

  def __init__(self):
    pass

  def delta(self, x):
    """Transition function
      Returns:
        True, if an arc was taken
        False, otherwise
    """
    if self._delta(x):
      self.lexeme += x
      return True
    else:
      return False

  def _delta(self, x):
    """Runs the state machine.
      Returns:
        True, if an arc was taken
        False, otherwise
    """
    pass

  def is_final(self):
    return True
