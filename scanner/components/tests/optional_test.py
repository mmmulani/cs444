import unittest

from ..concat import Concat
from ..one_or_more import OneOrMore
from ..optional import Optional
from ..string_dfa import String

class TestOptional(unittest.TestCase):

  def test_optional_char(self):
    machine = Optional(String('a'))
    self.assertTrue(machine.clone().accepts(''))
    self.assertTrue(machine.clone().accepts('a'))
    self.assertFalse(machine.clone().accepts('aa'))
    self.assertFalse(machine.clone().accepts('b'))

  def test_optional_prefix(self):
    machine = Concat(Optional(String('a')), OneOrMore(String('b')))
    self.assertTrue(machine.clone().accepts('b'))
    self.assertTrue(machine.clone().accepts('bbb'))
    self.assertTrue(machine.clone().accepts('ab'))
    self.assertTrue(machine.clone().accepts('ab'))
    self.assertFalse(machine.clone().accepts('a'))
    self.assertFalse(machine.clone().accepts('aab'))

if __name__ == '__main__':
  unittest.main()
