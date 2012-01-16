import unittest

from ..input_character import InputCharacter
from ..one_or_more import OneOrMore

class TestInputCharacter(unittest.TestCase):

  def test_input_character(self):
    for x in range(0,10) + [1, 12] + range(14, 128):
      self.assertTrue(InputCharacter().accepts(chr(x)))

    test_str = 'CS 444/644 - Compiler Construction'
    self.assertTrue(OneOrMore(InputCharacter()).accepts(test_str))

    self.assertFalse(InputCharacter().accepts('\n'))
    self.assertFalse(InputCharacter().accepts('\r'))

    bad_str = 'test\n'
    self.assertFalse(OneOrMore(InputCharacter()).accepts(bad_str))

if __name__ == '__main__':
  unittest.main()
