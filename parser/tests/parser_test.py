import unittest

from ..parser import Parser, ParsingError

class ParserTest(unittest.TestCase):
  def setUp(self):
    #TODO (gnleece) this will break if the test is not run from cs444 directory
    # ...not sure how to fix that?
    self.parser = Parser("parser/tests/sample_reduce", 
                         "parser/tests/sample_shift")
  
  def test_valid_tokens(self):
    '''Test sequences of tokens that are parsable'''
    self.parser.parse(["BOF", "id", "EOF"])
    self.parser.parse(["BOF", "id", "-", "id", "-", "id", "EOF"])
    self.parser.parse(["BOF", "(", "(", "id", "-", "id", ")", "-", "id", ")",
                       "-", "(", "id", "-", "id", ")", "EOF"])

  def test_invalid_tokens(self):
    '''Test sequences of tokens that are not parsable'''
    self.assertRaises(ParsingError, self.parser.parse, ["BOF", "-", "EOF"])
    self.assertRaises(ParsingError, self.parser.parse, ["id"])
    self.assertRaises(ParsingError, self.parser.parse, 
                      ["BOF", "id", "id", "id", "EOF"])
    self.assertRaises(ParsingError, self.parser.parse, 
                      ["BOF", "id", "(", "id", ")", "-", "id", "EOF"])

if __name__ == '__main__':
  unittest.main()
