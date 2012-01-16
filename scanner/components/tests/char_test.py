import unittest

from .. import char

class TestChar(unittest.TestCase):
  def setUp(self):
    self.machine = char.Char('d')

  def test_correct_character(self):
    self.assertTrue(self.machine.delta('d'))
    self.assertTrue(self.machine.is_final())

  def test_incorrect_character(self):
    self.assertFalse(self.machine.delta('x'))
    self.assertFalse(self.machine.is_final())

if __name__ == '__main__':
  unittest.main()
