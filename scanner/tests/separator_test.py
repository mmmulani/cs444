from .. import separator

import unittest

class SeparatorTest(unittest.TestCase):
  def test_separators(self):
    '''Test all valid separators.
    List taken from the Java Specification.
    '''
    separators = ['(', ')', '{', '}', '[', ']', ';', ',', '.']

    for s in separators:
      m = separator.Separator()
      self.assertTrue(m.accepts(s))
      self.assertEqual(m.lexeme, s)

  def test_non_separators(self):
    '''Test non-separators.
    Tests things that look like separators, but are not valid.
    '''
    non_separators = [
        '<', '>', '`']
    for s in non_separators:
      m = separator.Separator()
      self.assertFalse(m.accepts(s))

  def test_repeated_separators(self):
    '''Test repeating separators.'''
    m = separator.Separator()
    # First one should pass and be final.  Second character should fail.
    self.assertTrue(m.delta('('))
    self.assertTrue(m.is_final())
    self.assertFalse(m.delta('('))
    self.assertFalse(m.is_final())
    self.assertEqual(m.lexeme, '(')

    m = separator.Separator()
    # First one should pass and be final.  Second character should fail.
    self.assertTrue(m.delta('('))
    self.assertTrue(m.is_final())
    self.assertFalse(m.delta(')'))
    self.assertFalse(m.is_final())
    self.assertEqual(m.lexeme, '(')

    m = separator.Separator()
    # First one should pass and be final.  Second character should fail.
    self.assertTrue(m.delta('.'))
    self.assertTrue(m.is_final())
    self.assertFalse(m.delta('.'))
    self.assertFalse(m.is_final())
    self.assertEqual(m.lexeme, '.')

if __name__ == '__main__':
  unittest.main()
