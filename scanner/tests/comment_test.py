import unittest

from ..comment import Comment, EndOfLineComment, TraditionalComment

class TestComment(unittest.TestCase):
  star_passing_strs = [
    '/* tttt */',
    '/* ttt /* ttt */',
    '/*** ttt */',
    '/* ttt ***/',
    '/* */',
    '/* /*/',
    '/* // */',
    '/* test*test*/',
    '/* test*test**/',
    '/* test*t*/',
    '/* test/**/',
    '/**/',
    '/*/*/',
    '/* test/test/test*/',
    '/* test/test/test/*/',
    '/*////*/',
    '/** java doc */',
    '/*\n*/',
    '/* test\n*/',
    '/*\n*\n*/'
  ]

  star_failing_strs = [
    '/* //'
    '/*aaaaa/',
    '/*test*/*/',
    '/* test *///* test */',
    '/* test *//',
    '/* comment */ more stuff /* new comment */'
  ]

  single_passing_strs = [
    '// Simple comment\n',
    '//\n',
    '///test\n',
    '// Diff ending\r'
  ]

  single_failing_strs = [
    '// Comment without newline',
    '/ Missing a slash\n',
    'Missing both slashes\n'
  ]

  def test_end_of_line_comment(self):
    '''Test single line comments.'''
    for string in self.single_passing_strs:
      machine = EndOfLineComment()
      self.assertTrue(machine.accepts(string))
      self.assertTrue(machine.lexeme == string)

    for string in self.single_failing_strs:
      machine = EndOfLineComment()
      self.assertFalse(machine.accepts(string))

  def test_star_comments(self):
    '''Test /* comments */'''
    for string in self.star_passing_strs:
      machine = TraditionalComment()
      self.assertTrue(machine.accepts(string))
      self.assertTrue(machine.lexeme == string)

    for string in self.star_failing_strs:
      self.assertFalse(TraditionalComment().accepts(string))

  def test_comments(self):
    '''Test both types of comments.'''
    for string in self.star_passing_strs + self.single_passing_strs:
      machine = Comment()
      self.assertTrue(machine.accepts(string))
      self.assertTrue(machine.lexeme == string)

    for string in self.star_failing_strs + self.single_failing_strs:
      machine = Comment()
      self.assertFalse(machine.accepts(string))

if __name__ == '__main__':
  unittest.main()
