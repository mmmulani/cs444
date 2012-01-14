from dfa import DFA

class Char(DFA):
  char = None
  def __init__(self, c):
    self.char = c

  def _delta(self, x):
    return x == self.char and len(self.lexeme) == 0

  def is_final(self):
    return self.lexeme == self.char
