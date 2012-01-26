import unittest

from ..scanner import Scanner, Token

class TestScanner(unittest.TestCase):
  def test_simple_tokens(self):
    toks = Scanner.get_token_list('test test')
    self.assertListEqual([
        (Token.IDENTIFIER, 'test'),
        (Token.WHITESPACE, ' '),
        (Token.IDENTIFIER, 'test')],
        toks)
