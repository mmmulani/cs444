import unittest

from ..whitespace import LineTerminator, Whitespace
from ..one_or_more import OneOrMore

class TestWhitespace(unittest.TestCase):

  def test_line_terminator(self):
    self.assertTrue(LineTerminator().accepts('\n'))
    self.assertTrue(LineTerminator().accepts('\r'))
    self.assertTrue(LineTerminator().accepts('\r\n'))

    self.assertFalse(LineTerminator().accepts(' '))
    self.assertFalse(LineTerminator().accepts('\n\r'))
    self.assertFalse(LineTerminator().accepts('\n\n'))

  def test_whitespace(self):
    self.assertTrue(Whitespace().accepts(' '))
    self.assertTrue(Whitespace().accepts('\t'))
    self.assertTrue(Whitespace().accepts('\f'))
    self.assertTrue(Whitespace().accepts('\n'))
    self.assertTrue(Whitespace().accepts('\r'))
    self.assertTrue(Whitespace().accepts('\r\n'))
    self.assertTrue(OneOrMore(Whitespace()).accepts('\n\n  \t\t'))

    self.assertFalse(Whitespace().accepts('\n\r'))
    self.assertFalse(Whitespace().accepts(' a'))
    self.assertFalse(Whitespace().accepts('\n\t'))

if __name__ == '__main__':
  unittest.main()
