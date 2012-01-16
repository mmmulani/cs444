from composed_dfa import ComposedDFA

class Optional(ComposedDFA):
  def __init__(self, machine):
    self.machine = machine
    super(Optional, self).__init__()

  def is_final(self):
    return len(self.lexeme) == 0 or self.machine.is_final()

  def clone(self):
    return Optional(self.machine.clone())
