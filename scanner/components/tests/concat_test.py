import unittest

from ..concat import Concat
from ..one_or_more import OneOrMore
from ..optional import Optional
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

  def test_empty_prefixes(self):
    '''Test concat with multiple Optional prefixes'''
    machine = Concat(
      Optional(String('a')),
      Optional(String('b')),
      Optional(String('c')),
      Optional(String('d')),
      Optional(String('e')),
      String('f')
    )

    self.assertFalse(machine.is_final())
    self.assertTrue(machine.delta('a'))
    self.assertFalse(machine.is_final())
    self.assertTrue(machine.delta('f'))
    self.assertTrue(machine.is_final())

    self.assertTrue(machine.clone().accepts('f'))
    self.assertTrue(machine.clone().accepts('bf'))
    self.assertTrue(machine.clone().accepts('ef'))
    self.assertTrue(machine.clone().accepts('bcf'))
    self.assertTrue(machine.clone().accepts('abcdef'))

    optional_machine = Concat(
      Optional(String('a')),
      Optional(String('b')),
      Optional(String('c')),
      Optional(String('d'))
    )

    self.assertTrue(optional_machine.is_final())
    self.assertTrue(optional_machine.clone().accepts('a'))
    self.assertTrue(optional_machine.clone().accepts('b'))
    self.assertTrue(optional_machine.clone().accepts('c'))
    self.assertTrue(optional_machine.clone().accepts('d'))
    self.assertTrue(optional_machine.clone().accepts('ab'))
    self.assertTrue(optional_machine.clone().accepts('cd'))
    self.assertTrue(optional_machine.clone().accepts('abcd'))

    self.assertFalse(optional_machine.clone().accepts('af'))

if __name__ == '__main__':
  unittest.main()
