from ..string_literal import StringLiteral
from random import choice

import unittest

class StringLiteralTest(unittest.TestCase):

  def test_escape_chars(self):
    '''Test string literals with escape characters'''
    m = StringLiteral()

    self.assertTrue(m.clone().accepts('"\\t"'))
    self.assertTrue(m.clone().accepts('"\\n"'))
    self.assertTrue(m.clone().accepts('"\\\""'))
    self.assertTrue(m.clone().accepts('"\\\\"'))
    self.assertTrue(m.clone().accepts('"\\n\\n"'))

    self.assertFalse(m.clone().accepts('"\\"'))

  def test_random_string_literals(self):
    '''Test 100 random string literals of length 2'''
    normal_chars = [chr(x) for x in set(range(0, 128)) - set([10, 13, 34, 92])]
    escape_seqs = ['\\b', '\\t', '\\n', '\\f', '\\r', '\\"', "\\'", '\\\\']

    all_chars = normal_chars + escape_seqs
    m = StringLiteral()

    for x in range(0, 10):
      for y in range(0, 10):
        string_to_test = choice(all_chars) + choice(all_chars)
        self.assertTrue(m.clone().accepts('"' + string_to_test + '"'))

  def test_general_string_literals(self):
    '''Test valid and invalid simple string literals'''
    m = StringLiteral()

    self.assertTrue(m.clone().accepts('""'))
    self.assertTrue(m.clone().accepts('"W00t! CS444 scanner here."'))
    self.assertTrue(m.clone().accepts('"Newline escapes are allowed\\n.."'))
    self.assertTrue(m.clone().accepts(
      '"This is a 1000 character string literal. ' + ('!' * 959) + '"'
      ))

    self.assertFalse(m.clone().accepts('"But not newlines\nMore text"'))

    self.assertFalse(m.clone().accepts("'a'"))
    self.assertFalse(m.clone().accepts("'ab'"))
