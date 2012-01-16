import unittest

from ..java_letter import JavaLetter

class TestJavaLetter(unittest.TestCase):

  letters_range = set(range(65, 91) + range(97, 123) + [36, 95])
  
  def test_java_letter(self):
    for x in self.letters_range:
      self.assertTrue(JavaLetter().accepts(chr(x)))

  def test_non_java_letter(self):
    for x in set(range(0, 256)) - self.letters_range:
      self.assertFalse(JavaLetter().accepts(chr(x)))

if __name__ == '__main__':
  unittest.main()
