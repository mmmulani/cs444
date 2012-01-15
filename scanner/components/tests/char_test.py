import unittest

from .. import char

class TestChar(unittest.TestCase):
  def test_correct_character(self):
    machine = char.Char('d')
    self.assertTrue(machine.delta('d'))
    self.assertTrue(machine.is_final())

  def test_incorrect_character(self):
    machine = char.Char('d')
    self.assertFalse(machine.delta('x'))
    self.assertFalse(machine.is_final())

if __name__ == '__main__':
  unittest.main()
