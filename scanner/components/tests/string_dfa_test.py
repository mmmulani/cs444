import unittest

from ..string_dfa import String

class TestString(unittest.TestCase):

  def test_correct_character(self):
    machine = String('d')
    self.assertTrue(machine.delta('d'))
    self.assertTrue(machine.is_final())

  def test_incorrect_character(self):
    machine = String('d')
    self.assertFalse(machine.delta('x'))
    self.assertFalse(machine.is_final())

  def test_correct_string(self):
    machine = String('foobarbaz')
    self.assertTrue(machine.accepts_string('foobarbaz'))
    self.assertTrue(machine.is_final())

  def test_incorrect_string(self):
    machine = String('foobarbaz')
    self.assertFalse(machine.accepts_string('foofoo'))
    self.assertFalse(machine.is_final())

  def test_prefix_match(self):
    machine = String('abc')
    self.assertFalse(machine.accepts_string('abcd'))
    self.assertFalse(machine.is_final())

if __name__ == '__main__':
  unittest.main()
