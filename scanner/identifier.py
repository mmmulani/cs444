from components.composed_dfa import ComposedDFA
from components.concat import Concat
from components.java_digit import JavaDigit
from components.java_letter import JavaLetter
from components.one_of import OneOf
from components.zero_or_more import ZeroOrMore

class Identifier(ComposedDFA):
  """ An identifier is a JavaLetter followed by zero or more
      JavaLetters or JavaDigits. An identifier cannot be
      identical to any Keyword, to the BooleanLiteral, or
      the NullLiteral
  """

  # TODO (gnleece): exclude keywords, booleanliteral, nullliteral

  def __init__(self):
    self.machine = Concat(
        JavaLetter(), ZeroOrMore(OneOf(JavaLetter(), JavaDigit())))
    super(Identifier, self).__init__()
