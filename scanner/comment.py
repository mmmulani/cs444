from components.composed_dfa import ComposedDFA
from components.concat import Concat
from components.dfa import DFA
from components.input_character import InputCharacter
from components.one_of import OneOf
from components.string_dfa import String
from components.zero_or_more import ZeroOrMore
from whitespace import LineTerminator

class EndOfLineComment(ComposedDFA):
  def __init__(self):
    self.machine = Concat(
      String('//'),
      ZeroOrMore(InputCharacter()),
      LineTerminator()
    )
    super(EndOfLineComment, self).__init__()

class TraditionalComment(ComposedDFA):
  def __init__(self):
    self.machine = Concat(String('/*'), TraditionalCommentTail())
    super(TraditionalComment, self).__init__()

class TraditionalCommentTail(DFA):
  '''This manually reads input until it decides to stop rather than being made
    up of other DFAs.'''
  letters = [chr(x) for x in range(0, 128)]
  def __init__(self):
    self.done = False
    self.last_char = None
    super(TraditionalCommentTail, self).__init__()

  def _delta(self, x):
    if self.done:
      return False

    if x == '/' and self.last_char == '*':
      self.done = True

    if x in self.letters:
      self.last_char = x

    return x in self.letters

  def is_final(self):
    return self.done

  def clone(self):
    return TraditionalCommentTail()

class Comment(ComposedDFA):
  def __init__(self):
    self.machine = OneOf(TraditionalComment(), EndOfLineComment())

    super(Comment, self).__init__()
