import unittest

from ..scanner import Scanner, Token, TokenType

class TestScanner(unittest.TestCase):
  def test_simple_tokens(self):
    '''Test simple strings of tokens'''
    toks = Scanner.get_token_list('test test')
    self.assertEqual(self._add_file_tokens([
        Token(TokenType.IDENTIFIER, 'test'),
        Token(TokenType.WHITESPACE, ' '),
        Token(TokenType.IDENTIFIER, 'test')]),
        toks)

  def test_single_char_token(self):
    '''Test combination of single-character tokens'''
    toks = Scanner.get_token_list(' ')
    self.assertEqual(self._add_file_tokens([
      Token(TokenType.WHITESPACE, ' ')]),
      toks)

    toks = Scanner.get_token_list('t ')
    self.assertEqual(self._add_file_tokens([
        Token(TokenType.IDENTIFIER, 't'),
        Token(TokenType.WHITESPACE, ' ')]),
        toks)

    toks = Scanner.get_token_list('  ')
    self.assertEqual(self._add_file_tokens([
        Token(TokenType.WHITESPACE, ' '),
        Token(TokenType.WHITESPACE, ' ')]),
        toks)

  def test_precedence(self):
    '''Test precedence of tokens'''
    toks = Scanner.get_token_list('static')
    self.assertEqual(self._add_file_tokens([
      Token(TokenType.KEYWORD, 'static')]),
      toks)

    toks = Scanner.get_token_list('public')
    self.assertEqual(self._add_file_tokens([
      Token(TokenType.KEYWORD, 'public')]),
      toks)

    toks = Scanner.get_token_list('/* a comment */')
    self.assertEqual(self._add_file_tokens([
      Token(TokenType.COMMENT, '/* a comment */')]),
      toks)

  def _add_file_tokens(self, toks):
    return [Token.BOF_token()] + toks + [Token.EOF_token()]

