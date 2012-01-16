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
    raise Exception('Must override _delta()!')

  def is_final(self):
    raise Exception('Must override is_final()!')

  def clone(self):
    """Clone this DFA.
    Creates a new instance of this DFA, with an empty lexeme and the same
    parsing rules.
    """
    raise Exception('No clone() was defined!')

  def accepts_string(self, input):
    """Tests the string against the DFA. Returns true if the DFA accepts the
      entire input.
    """
    for x in input:
      if not self.delta(x):
        return False

    return self.is_final()
