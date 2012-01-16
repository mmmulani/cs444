from .. import operator

import unittest

class OperatorTest(unittest.TestCase):
  def test_operators(self):
    '''Test all the valid operators according to the Java spec.'''
    ops = [
        '=', '>', '<', '!', '~', '?', ':',
        '==', '<=', '>=', '!=', '&&', '||', '++', '--',
        '+', '-', '*', '/', '&', '|', '^', '%', '<<', '>>', '>>>',
        '+=', '-=', '*=', '/=', '&=', '|=', '^=', '%=', '<<=', '>>=',
        '>>>=']

    for op in ops:
      m = operator.Operator()
      self.assertTrue(m.accepts(op))
      self.assertEqual(m.lexeme, op)

  def test_non_operators(self):
    '''Test things that look like operators, but aren't valid ones.'''
    # TODO(songandrew): fix this
    self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()
