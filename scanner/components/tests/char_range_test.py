from .. import char_range

import unittest
import string

class CharRangeTest(unittest.TestCase):

  def test_digit_range(self):
    '''Test range of ASCII digits.'''
    # chr(48) == '0'; chr(57) == '9'
    m = char_range.CharRange(48, 57)
    for x in range(10):
      self.assertTrue(m.clone().accepts(str(x)))

    # Test boundaries
    self.assertFalse(m.clone().accepts(chr(47)))
    self.assertFalse(m.clone().accepts(chr(58)))

  def test_capital_range(self):
    '''Test the range of capital letters.'''
    # chr(65) == 'A'; chr(90) == 'Z'
    m = char_range.CharRange(65, 90)
    for x in string.ascii_uppercase:
      self.assertTrue(m.clone().accepts(x)) 

    # Should not accept any lowercase letters
    for x in string.ascii_lowercase:
      self.assertFalse(m.clone().accepts(x)) 

  def test_single_range(self):
    '''Test a range of length one.'''
    # chr(65) == 'A'
    m = char_range.CharRange(65, 65)
    self.assertTrue(m.clone().accepts('A'))

    self.assertFalse(m.clone().accepts('@'))
    self.assertFalse(m.clone().accepts('B'))
