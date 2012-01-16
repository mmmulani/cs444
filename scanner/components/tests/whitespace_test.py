import unittest

from ..whitespace import LineTerminator, Whitespace
from ..one_or_more import OneOrMore

class TestWhitespace(unittest.TestCase):

  def test_line_terminator(self):
    self.assertTrue(LineTerminator().accepts_string('\n'))
    self.assertTrue(LineTerminator().accepts_string('\r'))
    self.assertTrue(LineTerminator().accepts_string('\r\n'))

    self.assertFalse(LineTerminator().accepts_string(' '))
    self.assertFalse(LineTerminator().accepts_string('\n\r'))
    self.assertFalse(LineTerminator().accepts_string('\n\n'))

  def test_whitespace(self):
    self.assertTrue(Whitespace().accepts_string(' '))
    self.assertTrue(Whitespace().accepts_string('\t'))
    self.assertTrue(Whitespace().accepts_string('\f'))
    self.assertTrue(Whitespace().accepts_string('\n'))
    self.assertTrue(Whitespace().accepts_string('\r'))
    self.assertTrue(Whitespace().accepts_string('\r\n'))
    self.assertTrue(OneOrMore(Whitespace()).accepts_string('\n\n  \t\t'))

    self.assertFalse(Whitespace().accepts_string('\n\r'))
    self.assertFalse(Whitespace().accepts_string(' a'))
    self.assertFalse(Whitespace().accepts_string('\n\t'))

if __name__ == '__main__':
  unittest.main()
