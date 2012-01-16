from dfa import DFA

class ComposedDFA(DFA):
  """Blah"""
  def __init__(self):
    if not self.machine:
      raise Exception('self.machine must be set at initialization')

    super(ComposedDFA, self).__init__()

  def delta(self, x):
    return self.machine.delta(x)

  def is_final(self):
    return self.machine.is_final()

  def lexeme(self):
    return self.machine.lexeme()

  def recreate(self):
    return ComposedDFA(self.machine.recreate())
