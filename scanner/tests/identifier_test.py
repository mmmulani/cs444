import unittest

from ..identifier import Identifier

class TestIdentifier(unittest.TestCase):

  def test_good_identifiers(self):
    '''Test valid identifiers'''
    self.assertTrue(Identifier().accepts("a"))
    self.assertTrue(Identifier().accepts("abcdef"))
    self.assertTrue(Identifier().accepts("a123"))
    self.assertTrue(Identifier().accepts("abc_def"))
    self.assertTrue(Identifier().accepts("_foo"))
    self.assertTrue(Identifier().accepts("$foo"))
    self.assertTrue(Identifier().accepts("HELLO"))
    self.assertTrue(Identifier().accepts("$foo_123_abc"))

  def test_bad_identifiers(self):
    '''Test invalid identifiers'''
    
    # Identifiers can't start with numbers:
    self.assertFalse(Identifier().accepts("0"))
    self.assertFalse(Identifier().accepts("123"))
    self.assertFalse(Identifier().accepts("1foo"))

    # Identifiers can only contain A-Z, a-z, _, $
    self.assertFalse(Identifier().accepts("foo!"))
    self.assertFalse(Identifier().accepts("abc.def"))


  #TODO (gnleece): test no keywords
  #TODO (gnleece): test no booleanliteral, nullliteral

if __name__ == '__main__':
  unittest.main()
