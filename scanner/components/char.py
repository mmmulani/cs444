from dfa import DFA

class Char(DFA):
  def __init__(self, c):
    self.char = c
    super(Char, self).__init__()

  def _delta(self, x):
    return x == self.char and len(self.lexeme) == 0

  def is_final(self):
    return self.lexeme == self.char

  def clone(self):
    return Char(self.char)
