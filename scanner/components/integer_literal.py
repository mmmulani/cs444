from composed_dfa import ComposedDFA
from concat import Concat
from java_digit import JavaDigit
from octal_digit import OctalDigit
from one_of import OneOf
from one_of_chars import OneOfChars
from one_or_more import OneOrMore
from optional import Optional
from string_dfa import String
from zero_or_more import ZeroOrMore

class IntegerLiteral(ComposedDFA):
  def __init__(self):
    self.machine = Concat(
      OneOf(DecimalNumeral(), HexNumeral(), OctalNumeral()),
      Optional(OneOfChars(list('lL')))
    )

    super(IntegerLiteral, self).__init__()

class DecimalNumeral(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(
      String('0'),
      Concat(OneOfChars('123456789'), ZeroOrMore(JavaDigit()))
    )

    super(DecimalNumeral, self).__init__()

class HexNumeral(ComposedDFA):
  def __init__(self):
    self.machine = Concat(
      OneOf(String('0x'), String('0X')),
      OneOrMore(OneOfChars('0123456789abcdefABCDEF'))
    )

    super(HexNumeral, self).__init__()

class OctalNumeral(ComposedDFA):
  def __init__(self):
    self.machine = Concat(String('0'), OneOrMore(OctalDigit()))

    super(OctalNumeral, self).__init__()
