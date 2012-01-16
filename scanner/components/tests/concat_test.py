import unittest

from ..concat import Concat
from ..one_or_more import OneOrMore
from ..string_dfa import String
from ..zero_or_more import ZeroOrMore

class TestConcat(unittest.TestCase):
  def test_simple_concat(self):
    '''Test concatenating two strings.'''
    m = Concat(String('x'), String('y'))
    self.assertTrue(m.delta('x'))
    self.assertFalse(m.is_final())
    self.assertTrue(m.delta('y'))
    self.assertTrue(m.is_final())

    # DFA should fail when passed more input.
    self.assertFalse(m.delta('y'))
    self.assertFalse(m.is_final())

  def test_empty_prefix(self):
    '''Test concat with ZeroOrMore prefix'''
    machine = Concat(ZeroOrMore(String('a')), String('b'))
    self.assertTrue(machine.clone().accepts('b'))
    self.assertTrue(machine.clone().accepts('ab'))
    self.assertTrue(machine.clone().accepts('aaab'))

    self.assertFalse(machine.clone().accepts('a'))
    self.assertFalse(machine.clone().accepts('bb'))
    self.assertFalse(machine.clone().accepts(''))

if __name__ == '__main__':
  unittest.main()
