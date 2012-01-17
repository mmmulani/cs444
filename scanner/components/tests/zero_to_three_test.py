from .. import zero_to_three

import unittest

class ZeroToThree(unittest.TestCase):
  def test_valid_digits(self):
    '''Test valid 0-3 digits'''
    m = zero_to_three.ZeroToThree()

    for x in range(4):
      self.assertTrue(m.clone().accepts(str(x)))

  def test_non_digits(self):
    '''Test non-0 to 3 digits'''
    m = zero_to_three.ZeroToThree()

    for x in range(4, 10):
      self.assertFalse(m.clone().accepts(str(x)))
