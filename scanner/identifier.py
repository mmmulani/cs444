from components.dfa import DFA

class Identifier(DFA):
  """ An identifier is a JavaLetter followed by zero or more
      JavaLetters or JavaDigits. An identifier cannot be
      identical to any Keyword, to the BooleanLiteral, or
      the NullLiteral
  """

  JAVA_LETTERS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_$')
  JAVA_DIGITS = set('0123456789')
  def __init__(self):
    super(Identifier, self).__init__()

  def _delta(self, x):
    if len(self.lexeme) == 0:
      return x in self.JAVA_LETTERS

    return x in self.JAVA_LETTERS or x in self.JAVA_DIGITS

  def is_final(self):
    return len(self.lexeme) > 0

  def clone(self):
    return Identifier()
