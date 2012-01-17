from composed_dfa import ComposedDFA
from concat import Concat
from java_digit import JavaDigit
from one_of import OneOf
from one_or_more import OneOrMore
from optional import Optional
from string_dfa import String

class Digits(ComposedDFA):
  def __init__(self):
    self.machine = OneOrMore(JavaDigit())
    # NOTE: This must be called last as self.machine must be set.
    super(Digits, self).__init__()

class FloatTypeSuffix(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(String("f"), String("F"), String("d"), String("D"))
    # NOTE: This must be called last as self.machine must be set.
    super(FloatTypeSuffix, self).__init__()

class SignedInteger(ComposedDFA):
  def __init__(self):
    self.machine = Concat(Optional(OneOf(String("+"), String("-"))), Digits())
    # NOTE: This must be called last as self.machine must be set.
    super(SignedInteger, self).__init__()

class ExponentPart(ComposedDFA):
  def __init__(self):
    self.machine = Concat(OneOf(String("e"), String("E")), SignedInteger())
    # NOTE: This must be called last as self.machine must be set.
    super(ExponentPart, self).__init__()
