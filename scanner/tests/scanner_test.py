import unittest

from ..scanner import Scanner, Token

class TestScanner(unittest.TestCase):
  def test_simple_tokens(self):
    '''Test simple strings of tokens'''
    toks = Scanner.get_token_list('test test')
    self.assertListEqual([
        (Token.IDENTIFIER, 'test'),
        (Token.WHITESPACE, ' '),
        (Token.IDENTIFIER, 'test')],
        toks)

  def test_single_char_token(self):
    '''Test combination of single-character tokens'''
    toks = Scanner.get_token_list(' ')
    self.assertListEqual([(Token.WHITESPACE, ' ')], toks)

    toks = Scanner.get_token_list('t ')
    self.assertListEqual([
        (Token.IDENTIFIER, 't'),
        (Token.WHITESPACE, ' ')],
        toks)

    toks = Scanner.get_token_list('  ')
    self.assertListEqual([
        (Token.WHITESPACE, ' '),
        (Token.WHITESPACE, ' ')],
        toks)

  def test_precedence(self):
    '''Test precedence of tokens'''
    toks = Scanner.get_token_list('static')
    self.assertListEqual([(Token.KEYWORD, 'static')], toks)

    toks = Scanner.get_token_list('public')
    self.assertListEqual([(Token.KEYWORD, 'public')], toks)

    toks = Scanner.get_token_list('/* a comment */')
    self.assertListEqual([(Token.COMMENT, '/* a comment */')], toks)
