import unittest

from ..java_digit import JavaDigit

class TestJavaDigit(unittest.TestCase):

  digits_range = set(range(48,58))  
  def test_java_digit(self):
    for x in self.digits_range:
      self.assertTrue(JavaDigit().accepts(chr(x)))

  def test_non_java_digit(self):
    for x in set(range(0, 256)) - self.digits_range:
      self.assertFalse(JavaDigit().accepts(chr(x)))
  
    self.assertFalse(JavaDigit().accepts('123'))

if __name__ == '__main__':
  unittest.main()
