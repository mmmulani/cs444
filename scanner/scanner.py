import comment
import identifier
import keyword
import literal
import operator
import separator
import whitespace

class Token:
  '''Token enumeration.'''
  WHITESPACE = 'WHITESPACE'
  COMMENT = 'COMMENT'
  IDENTIFIER = 'IDENTIFIER'
  KEYWORD = 'KEYWORD'
  LITERAL = 'LITERAL'
  SEPARATOR = 'SEPARATOR'
  OPERATOR = 'OPERATOR'

class Scanner(object):
  '''Scanner object
  Responsible for scanning/tokenizing valid JOS programs given as a string'''

  # These machines are kept in priority order.
  machines = [
      operator.Operator(),
      separator.Separator(),
      literal.Literal(),
      keyword.Keyword(),
      identifier.Identifier(),
      comment.Comment(),
      whitespace.Whitespace()]

  token_map = {
      operator.Operator: Token.OPERATOR,
      separator.Separator: Token.SEPARATOR,
      literal.Literal: Token.LITERAL,
      keyword.Keyword: Token.KEYWORD,
      identifier.Identifier: Token.IDENTIFIER,
      comment.Comment: Token.COMMENT,
      whitespace.Whitespace: Token.WHITESPACE
  }

  @staticmethod
  def get_token_list(s):
    s = Scanner(s)
    return list(s.scan())

  def __init__(self, s):
    self.s = s

  def scan(self):
    '''Generator which produces tokens'''
    i = 0

    while i < len(self.s):
      cur_machines = [m.clone() for m in Scanner.machines]
      last_final = None
      while len(cur_machines) > 0 and i < len(self.s):
        c = self.s[i]
        cur_machines = [m for m in cur_machines if m.delta(c)]
        final_tokens = [ix for ix, m in enumerate(cur_machines) if m.is_final()]
        if len(final_tokens) > 0:
          # Keep track of the final token with the highest priority.
          last_final = self._get_token_from_machine(
              cur_machines[final_tokens[0]])
        i += 1

      if last_final:
        # No more valid machines.
        yield last_final
        if i < len(self.s):
          i -= 1
      else:
        # Scanning error.
        raise Exception('Scanning error: {0}', self.s[i:])

  def _get_token_from_machine(self, m):
    return (Scanner.token_map[type(m)], m.lexeme)
