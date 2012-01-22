import unittest

from ..literal import Literal

class TestLiteral(unittest.TestCase):

  def test_valid_literals(self):
    '''Test valid literals'''
    m = Literal()

    self.assertTrue(m.clone().accepts("123"))
    self.assertTrue(m.clone().accepts("0"))
    self.assertTrue(m.clone().accepts("0xDEADBEEF"))
    self.assertTrue(m.clone().accepts("0327"))
    self.assertTrue(m.clone().accepts("1.337"))
    self.assertTrue(m.clone().accepts("69e+96"))
    self.assertTrue(m.clone().accepts("true"))
    self.assertTrue(m.clone().accepts("'a'"))
    self.assertTrue(m.clone().accepts("'\\t'"))
    self.assertTrue(m.clone().accepts("\"hello world\""))
    self.assertTrue(m.clone().accepts("\"\""))
    self.assertTrue(m.clone().accepts("\"TRUE\""))
    self.assertTrue(m.clone().accepts("null"))
    
  def test_invalid_literals(self):
    '''Test invalid literals'''
    m = Literal()

    self.assertFalse(m.clone().accepts("0x"))
    self.assertFalse(m.clone().accepts("''"))
    self.assertFalse(m.clone().accepts("TRUE"))
    self.assertFalse(m.clone().accepts("\"foo"))
    self.assertFalse(m.clone().accepts("False"))
    self.assertFalse(m.clone().accepts("'abc'"))
    self.assertFalse(m.clone().accepts("0.222.f"))
    self.assertFalse(m.clone().accepts("NULL"))
    self.assertFalse(m.clone().accepts("herpderp\""))


if __name__ == '__main__':
  unittest.main()
