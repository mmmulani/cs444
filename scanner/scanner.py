import comment
import identifier
import keyword
import literal
import operator_dfa
import separator
import whitespace

class Token(object):
  '''A single token'''
  def __init__(self, type, lex):
    self.type = type
    self.lexeme = lex

  def __repr__(self):
    return str((self.type, self.lexeme))
  def __str__(self):
    return str((self.type, self.lexeme))

class Scanner(object):
  '''Scanner object
  Responsible for scanning/tokenizing valid JOS programs given as a string

  EXAMPLE 1:
    import scanner
    s = scanner.Scanner('this is my string')
    for t in s.scan():
      print t

  EXAMPLE 2:
    import scanner
    tokens = scanner.Scanner.get_token_list('this string')
    assertEqual(tokens[0], (Token.IDENTIFIER, 'this'))
    assertEqual(tokens[1], (Token.WHITESPACE, ' '))
    assertEqual(tokens[2], (Token.IDENTIFIER, 'string'))
  '''

  # These machines are kept in priority order.
  machines = [
      operator_dfa.Operator(),
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
    '''Generator which produces one token at a time.'''
    i = 0
    yield Token('BOF', 'BOF')
    while i < len(self.s):
      tok = self._get_next_token(i)
      if tok is None:
        # Scanning error.
        raise Exception('Scanning error: <{0}>'.format(self.s[i:]))
      yield tok

      i += len(tok.lexeme)
    yield Token('EOF', 'EOF')

  def _get_next_token(self, i):
    '''Get the next token start from position i of the string'''
    cur_machines = [m.clone() for m in Scanner.machines]
    last_final = None

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
    return Token(TokenType.token_map[type(m)], m.lexeme)

class TokenConverter:
  @staticmethod
  def convert(toks):
    '''Convert a list of tokens into their more specific types'''
    ret = []
    for t in toks:
      if t.type == TokenType.WHITESPACE or t.type == TokenType.COMMENT:
        # Strip whitespace from input.
        continue
      ret.append(TokenConverter._convert_token(t))
    return ret

  @staticmethod
  def _convert_token(t):
    if t.type == TokenType.IDENTIFIER:
      return t
    elif t.type == TokenType.SEPARATOR:
      return Token(t.lexeme, t.lexeme)
      # return Token(TokenConverter._get_separator_type(t.lexeme), t.lexeme)
    elif t.type == TokenType.OPERATOR:
      return Token(t.lexeme, t.lexeme)
      # return Token(TokenConverter._get_operator_type(t.lexeme), t.lexeme)
    elif t.type == TokenType.KEYWORD:
      return Token(t.lexeme, t.lexeme)
      # return Token(TokenConverter._get_keyword_type(t.lexeme), t.lexeme)
    elif t.type == TokenType.LITERAL:
      return Token('StringLiteral', t.lexeme)

class TokenType:
  '''Enumeration of token types.'''
  # High-level token types.
  WHITESPACE = 'Whitespace'
  COMMENT = 'Comment'
  IDENTIFIER = 'Identifier'
  KEYWORD = 'Keyword'
  LITERAL = 'Literal'
  SEPARATOR = 'Separator'
  OPERATOR = 'Operator'

  token_map = {
      operator_dfa.Operator: OPERATOR,
      separator.Separator: SEPARATOR,
      literal.Literal: LITERAL,
      keyword.Keyword: KEYWORD,
      identifier.Identifier: IDENTIFIER,
      comment.Comment: COMMENT,
      whitespace.Whitespace: WHITESPACE
  }

  # Separator types.
  LBRACKET = '('
  RBRACKET = ')'
  LBRACE = '{'
  RBRACE = '}'
  LSQUARE = '['
  RSQUARE = ']'
  SEMICOLON = ';'
  COMMA = ','
  DOT = '.'

  separator_map = {
      '(': LBRACKET,
      ')': RBRACKET,
      '{': LBRACE,
      '}': RBRACE,
      '[': LSQUARE,
      ']': RSQUARE,
      ';': SEMICOLON,
      ',': COMMA,
      '.': DOT
  }
