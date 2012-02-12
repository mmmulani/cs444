import unittest

from ..parser import Parser, ParsingError
from ...scanner.scanner import Token, TokenType

class ParserTest(unittest.TestCase):
  def setUp(self):
    #TODO (gnleece) this will break if the test is not run from cs444 directory
    # ...not sure how to fix that?
    self.parser = Parser('parser/tests/sample_reduce',
                         'parser/tests/sample_shift')

  def test_valid_tokens(self):
    '''Test sequences of tokens that are parsable'''
    self.parser.parse(self._add_file_tokens([Token('id', 'x')]))
    self.parser.parse(self._add_file_tokens(
        self._create_token_list(['id', '-', 'id', '-', 'id'])))
    self.parser.parse(self._add_file_tokens(
        self._create_token_list([
            '(', '(', 'id', '-', 'id', ')', '-', 'id', ')', '-', '(', 'id',
            '-', 'id', ')'])))

  def test_invalid_tokens(self):
    '''Test sequences of tokens that are not parsable'''
    self.assertRaises(ParsingError, self.parser.parse,
        self._add_file_tokens(self._create_token_list(['-'])))
    self.assertRaises(ParsingError, self.parser.parse,
        self._create_token_list(['id']))
    self.assertRaises(ParsingError, self.parser.parse,
        self._add_file_tokens(self._create_token_list(['id', 'id', 'id'])))
    self.assertRaises(ParsingError, self.parser.parse,
        self._add_file_tokens(self._create_token_list(
          ['id', '(', 'id', ')', '-', 'id'])))

  def _add_file_tokens(self, toks):
    return [Token.BOF_token()] + toks + [Token.EOF_token()]

  def _create_token_list(self, strs):
    return [Token(x, x) for x in strs]

if __name__ == '__main__':
  unittest.main()
