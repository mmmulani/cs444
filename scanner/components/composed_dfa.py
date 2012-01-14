from dfa import DFA

class ComposedDFA(DFA):
  """Blah"""

  machine = None

  def delta(self, x):
    return self.machine.delta(x)

  def is_final(self):
    return self.machine.is_final()

  def lexeme(self):
    return self.machine.lexeme()
