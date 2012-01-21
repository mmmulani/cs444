from composed_dfa import ComposedDFA
from concat import Concat
from dfa import DFA
from string_dfa import String

class StringLiteralBody(DFA):
  '''A DFA to match the text in a string literal. (the text in double-quotes)
    It is a hard-coded state machine so that it can be very fast.
  '''
  string_characters = set([chr(x) for x in set(range(0, 128)) -
    set([10, 13, 34, 92])])
  escape_characters = set(['b', 't', 'n', 'f', 'r', '"', "'", '\\', '0', '1',
    '2', '3', '4', '5', '6', '7'])
  def __init__(self):
    self.next_should_be_escape = False
    super(StringLiteralBody, self).__init__()

  def _delta(self, x):
    '''
      In the case that the character after the escape is an octal digit, we
      don't have to make sure that the following digits make up a valid octal
      number as they will just be parsed as valid characters.
    '''
    if self.next_should_be_escape:
      if x in self.escape_characters:
        self.next_should_be_escape = False
        return True
      return False

    if x == '\\':
      self.next_should_be_escape = True
      return True

    return x in self.string_characters

  def is_final(self):
    return not self.next_should_be_escape

  def clone(self):
    return StringLiteralBody()

class StringLiteral(ComposedDFA):
  """ The String Literal DFA.
    Example tokens: "lol"
  """

  """ String character is defined as an input character minus double-quote (34)
    and slash (92).
  """
  def __init__(self):
    self.machine = Concat(
      String('"'),
      StringLiteralBody(),
      String('"'))

    super(StringLiteral, self).__init__()
