from .. import octal_digit

import unittest

class OctalDigitTest(unittest.TestCase):
  def test_octal_digit(self):
    '''Test all octal digits'''
    m = octal_digit.OctalDigit()
    
    for x in range(8):
      self.assertTrue(m.clone().accepts(str(x)))

  def test_non_octal(self):
    '''Test non-octal digits'''
    m = octal_digit.OctalDigit()
    self.assertFalse(m.clone().accepts('8'))
    self.assertFalse(m.clone().accepts('9'))
