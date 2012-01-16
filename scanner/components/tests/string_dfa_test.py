import unittest

from ..string_dfa import String

class TestString(unittest.TestCase):

  def test_correct_character(self):
    '''Test correct character.'''

    machine = String('d')
    self.assertTrue(machine.delta('d'))
    self.assertTrue(machine.is_final())

    # If we pass the correct character again, it should fail.
    self.assertFalse(machine.delta('d'))
    self.assertFalse(machine.is_final())
    self.assertEqual(machine.lexeme, 'd')

  def test_incorrect_character(self):
    '''Test incorrect character.'''

    machine = String('d')
    self.assertFalse(machine.delta('x'))
    self.assertFalse(machine.is_final())

    # If we pass the correct character now, it should still fail.
    self.assertFalse(machine.delta('d'))
    self.assertFalse(machine.is_final())
    self.assertEqual(machine.lexeme, '')

  def test_correct_string(self):
    '''Test correct string.'''

    machine = String('foobarbaz')
    self.assertTrue(machine.accepts('foobarbaz'))
    self.assertTrue(machine.is_final())

    # DFA should not accept another copy of the string.
    self.assertFalse(machine.accepts('foobarbaz'))
    self.assertFalse(machine.is_final())

  def test_incorrect_string(self):
    '''Test incorrect string.'''

    machine = String('foobarbaz')
    self.assertFalse(machine.accepts('foofoo'))
    self.assertFalse(machine.is_final())

  def test_prefix_match(self):
    '''Test when M has string as a prefix.'''

    machine = String('abc')
    # Machine should accept up to the matching prefix.
    self.assertTrue(machine.delta('a'))
    self.assertTrue(machine.delta('b'))
    self.assertTrue(machine.delta('c'))
    self.assertTrue(machine.is_final())

    # Machine should fail after the string is no longer a prefix.
    self.assertFalse(machine.delta('d'))
    self.assertFalse(machine.is_final())

if __name__ == '__main__':
  unittest.main()
