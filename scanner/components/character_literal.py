from composed_dfa import ComposedDFA
from concat import Concat
from escape_sequence import EscapeSequence
from one_of import OneOf
from one_of_chars import OneOfChars
from string_dfa import String

class CharacterLiteral(ComposedDFA):
  """ The Character Literal DFA.
    Example: 'a'
  """

  """ Single character is defined as an input character minus single-quote (39)
    and slash (92).
  """
  single_characters = [chr(x) for x in set(range(0, 128)) -
    set([10, 13, 39, 92])]
  def __init__(self):
    self.machine = Concat(
      String('\''),
      OneOf(OneOfChars(self.single_characters), EscapeSequence()),
      String('\''))

    super(CharacterLiteral, self).__init__()
