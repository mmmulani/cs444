import unittest

from ..concat import Concat
from ..one_or_more import OneOrMore
from ..string_dfa import String
from ..zero_or_more import ZeroOrMore

class TestConcat(unittest.TestCase):

  def test_empty_prefix(self):
    machine = Concat(ZeroOrMore(String('a')), String('b'))
    self.assertTrue(machine.clone().accepts('b'))
    self.assertTrue(machine.clone().accepts('aaab'))
    self.assertFalse(machine.clone().accepts('a'))
    self.assertFalse(machine.clone().accepts('bb'))
    self.assertFalse(machine.clone().accepts(''))

if __name__ == '__main__':
  unittest.main()
