from dfa import DFA

class JavaLetter(DFA):
  """ Recognizes the "Java letter" characters, which are
      the uppercase letters (A-Z), lowercase letters (a-z),
      underscore (_) and dollar sign ($)
  """
  java_letters = set(
    [chr(x) for x in (range(65,91) + range(97,123) + [36, 95])])
  def __init__(self):
    super(JavaLetter, self).__init__()

  def _delta(self, x):
    return (x in self.java_letters) and len(self.lexeme) == 0

  def is_final(self):
    return len(self.lexeme) == 1

  def clone(self):
    return JavaLetter()
