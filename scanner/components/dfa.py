class DFA(object):
  """Blah"""

  def __init__(self):
    self.lexeme = ''

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
    raise Exception('No _delta() was defined!')

  def is_final(self):
    raise Exception('No is_final() was defined!')

  def recreate(self):
    """Creates a new instance of this DFA, with an empty lexeme and the same
      parsing rules."""
    raise Exception('No recreate() was defined!')
