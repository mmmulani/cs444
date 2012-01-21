import dfa
import types

class OneOfChars(dfa.DFA):
  '''Recognize a single character based on the list of characters provided.
    Examples:
      OneOfChars(['1', 'a', '!'])
      OneOfChars(list('12345'))
  '''

  def __init__(self, chars):
    ''' Micro-optimize the case where we are cloning. This ends up saving us a
      lot of time overall.
    '''
    if isinstance(chars, types.ListType):
      self.chars = set(chars)
    else:
      self.chars = chars

    super(OneOfChars, self).__init__()

  def _delta(self, x):
    return (x in self.chars) and len(self.lexeme) == 0

  def is_final(self):
    return len(self.lexeme) == 1

  def clone(self):
    return OneOfChars(self.chars)
