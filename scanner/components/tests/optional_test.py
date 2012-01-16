import unittest

from ..concat import Concat
from ..one_or_more import OneOrMore
from ..optional import Optional
from ..string import String
from ..zero_or_more import ZeroOrMore

class TestOptional(unittest.TestCase):

  def test_optional_char(self):
    machine = Optional(String('a'))
    self.assertTrue(machine.clone().accepts_string(''))
    self.assertTrue(machine.clone().accepts_string('a'))
    self.assertFalse(machine.clone().accepts_string('aa'))
    self.assertFalse(machine.clone().accepts_string('b'))

  def test_optional_prefix(self):
    machine = Concat(Optional(String('a')), OneOrMore(String('b')))
    self.assertTrue(machine.clone().accepts_string('b'))
    self.assertTrue(machine.clone().accepts_string('bbb'))
    self.assertTrue(machine.clone().accepts_string('ab'))
    self.assertTrue(machine.clone().accepts_string('ab'))
    self.assertFalse(machine.clone().accepts_string('a'))
    self.assertFalse(machine.clone().accepts_string('aab'))

if __name__ == '__main__':
  unittest.main()
