from .. import operator

import unittest

class OperatorTest(unittest.TestCase):
  def test_operators(self):
    '''Test all valid operators.
    List taken from the Java Specification.
    '''
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
    '''Test non-operators.
    Tests things that look like operators, but are not valid operators.
    '''
    non_ops = [
        '=<', '=>', '!!=', '=!', '<<<=', '&&=', '+-', '<<<']

    for op in non_ops:
      m = operator.Operator()
      self.assertFalse(m.accepts(op))

if __name__ == '__main__':
  unittest.main()
