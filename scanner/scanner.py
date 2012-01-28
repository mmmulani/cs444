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

  token_map = {
      operator.Operator: OPERATOR,
      separator.Separator: SEPARATOR,
      literal.Literal: LITERAL,
      keyword.Keyword: KEYWORD,
      identifier.Identifier: IDENTIFIER,
      comment.Comment: COMMENT,
      whitespace.Whitespace: WHITESPACE
  }

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
      tok = self._get_next_token(i)
      if tok is None:
        # Scanning error.
        raise Exception('Scanning error: <{0}>'.format(self.s[i:]))
      yield tok

      i += len(tok[1])

  def _get_next_token(self, i):
    '''Get the next token start from position i of the string'''
    cur_machines = [m.clone() for m in Scanner.machines]
    last_final = None
    l = 0

    for c in self.s[i:]:
      cur_machines = [m for m in cur_machines if m.delta(c)]
      final_token_ix = [ix for ix, m in enumerate(cur_machines)
          if m.is_final()]
      if len(final_token_ix) > 0:
        # Keep track of the final token with the highest precedence.
        last_final = self._get_token_from_machine(
            cur_machines[final_token_ix[0]])

      if len(cur_machines) == 0:
        break

    return last_final

  def _get_token_from_machine(self, m):
    return (Token.token_map[type(m)], m.lexeme)
