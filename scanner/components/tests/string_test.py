import unittest

from ..string import String

class TestString(unittest.TestCase):

  def test_correct_character(self):
    machine = string.String('d')
    self.assertTrue(machine.delta('d'))
    self.assertTrue(machine.is_final())

  def test_incorrect_character(self):
    machine = string.String('d')
    self.assertFalse(machine.delta('x'))
    self.assertFalse(machine.is_final())

  def test_correct_string(self):
    machine = string.String('foobarbaz')
    self.assertTrue(machine.accepts_string('foorbarbaz'))
    self.assertTrue(machine.is_final())

  def test_incorrect_string(self):
    machine = string.String('foobarbaz')
    self.assertFalse(machine.accepts_string('foofoo'))
    self.assertFalse(machine.is_final())

if __name__ == '__main__':
  unittest.main()
