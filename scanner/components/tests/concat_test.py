import unittest

from ..concat import Concat
from ..one_or_more import OneOrMore
from ..string_dfa import String
from ..zero_or_more import ZeroOrMore

class TestConcat(unittest.TestCase):

  def test_empty_prefix(self):
    machine = Concat(ZeroOrMore(String('a')), String('b'))
    self.assertTrue(machine.clone().accepts_string('b'))
    self.assertTrue(machine.clone().accepts_string('aaab'))
    self.assertFalse(machine.clone().accepts_string('a'))
    self.assertFalse(machine.clone().accepts_string('bb'))
    self.assertFalse(machine.clone().accepts_string(''))

if __name__ == '__main__':
  unittest.main()
