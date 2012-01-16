from dfa import DFA

class JavaDigit(DFA):
  """ Recognizes the digits 0-9 """

  java_digits = set([chr(x) for x in range(48,58)])
  def __init__(self):
    super(JavaDigit, self).__init__()

  def _delta(self, x):
    return (x in self.java_digits) and len(self.lexeme) == 0

  def is_final(self):
    return len(self.lexeme) == 1

  def clone(self):
    return JavaDigit()
