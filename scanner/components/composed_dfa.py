from dfa import DFA

class ComposedDFA(DFA):
  """Blah"""
  def __init__(self):
    self.machine = None
    super(ComposedDFA, self).__init__()

  def delta(self, x):
    return self.machine.delta(x)

  def is_final(self):
    return self.machine.is_final()

  def lexeme(self):
    return self.machine.lexeme()

  def clone(self):
    return ComposedDFA(self.machine.clone())
