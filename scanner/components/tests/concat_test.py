import unittest

from ..char import Char
from ..concat import Concat
from ..one_or_more import OneOrMore
from ..zero_or_more import ZeroOrMore

class TestConcat(unittest.TestCase):

  def test_empty_prefix(self):
    machine = Concat(ZeroOrMore(Char('a')), Char('b'))
    self.assertTrue(machine.recreate().accepts_string('b'))
    self.assertTrue(machine.recreate().accepts_string('aaab'))
    self.assertFalse(machine.recreate().accepts_string('a'))
    self.assertFalse(machine.recreate().accepts_string('bb'))
    self.assertFalse(machine.recreate().accepts_string(''))

if __name__ == '__main__':
  unittest.main()
