from ..character_literal import CharacterLiteral

import unittest

class CharacterLiteralTest(unittest.TestCase):

  def test_escape_chars(self):
    '''Test character literals with escape characters'''
    m = CharacterLiteral()

    self.assertTrue(m.clone().accepts("'\\t'"))
    self.assertTrue(m.clone().accepts("'\\n'"))
    self.assertTrue(m.clone().accepts("'\\''"))
    self.assertTrue(m.clone().accepts("'\\\\'"))

    self.assertFalse(m.clone().accepts("'\\'"))

  def test_char_literal(self):
    '''Test some expected and unexpected char literals'''
    m = CharacterLiteral()

    for x in set(range(0, 128)) - set([10, 13, 39, 92]):
      self.assertTrue(m.clone().accepts("'" + chr(x) + "'"))

    self.assertFalse(m.clone().accepts("'ab'"))
    self.assertFalse(m.clone().accepts("'a"))
    self.assertFalse(m.clone().accepts("''"))
    self.assertFalse(m.clone().accepts("a"))
    self.assertFalse(m.clone().accepts('"a"'))
