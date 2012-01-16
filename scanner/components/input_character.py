from dfa import DFA

class InputCharacter(DFA):
  """This DFA is meant to recognize any ASCII character except the carriage
    return (13) and line feed (10).
  """
  letters = set([chr(x) for x in (range(0,10) + [11, 12] + range(14, 128))])
  def __init__(self):
    super(InputCharacter, self).__init__()

  def _delta(self, x):
    return (x in self.letters) and len(self.lexeme) == 0

  def is_final(self):
    return len(self.lexeme) == 1

  def clone(self):
    return InputCharacter()
