from .. import escape_sequence

import unittest

class EscapeSequenceTest(unittest.TestCase):

  def test_simple_escape(self):
    '''Test simple escape characters'''
    m = escape_sequence.EscapeSequence()

    self.assertTrue(m.clone().accepts('\\b'))
    self.assertTrue(m.clone().accepts('\\t'))
    self.assertTrue(m.clone().accepts('\\n'))
    self.assertTrue(m.clone().accepts('\\f'))
    self.assertTrue(m.clone().accepts('\\r'))
    self.assertTrue(m.clone().accepts('\\"'))
    self.assertTrue(m.clone().accepts("\\'"))
    self.assertTrue(m.clone().accepts('\\\\'))

  def test_simple_octal_escape(self):
    '''Test simple octal escapes'''
    m = escape_sequence.EscapeSequence()

    # Test octal escapes of one digit long.
    for x in range(8):
      self.assertTrue(m.clone().accepts('\\' + str(x)))

    # Test octal escapes of two digits long.
    for x in range(8):
      for y in range(8):
        self.assertTrue(m.clone().accepts('\\' + str(x) + str(y)))

    # Test octal escapes of two digits long.
    for x in range(4):
      for y in range(8):
        for z in range(8):
          self.assertTrue(m.clone().accepts('\\' + str(x) + str(y) + str(z)))

  def test_non_escapes(self):
    '''Test invalid escape characters'''
    m = escape_sequence.EscapeSequence()

    self.assertFalse(m.clone().accepts('\\a'))
    self.assertFalse(m.clone().accepts('\\c'))
    self.assertFalse(m.clone().accepts('\\d'))
    self.assertFalse(m.clone().accepts('\\e'))
    self.assertFalse(m.clone().accepts('\\g'))
    self.assertFalse(m.clone().accepts('\\h'))
    self.assertFalse(m.clone().accepts('\\>'))
    self.assertFalse(m.clone().accepts('\\<'))
    self.assertFalse(m.clone().accepts('\\!'))

  def test_non_octals(self):
    '''Test invalid octal escapes'''
    m = escape_sequence.EscapeSequence()

    # Test invalid one-digit octals.
    self.assertFalse(m.clone().accepts('\\8'))
    self.assertFalse(m.clone().accepts('\\9'))

    # Test invalid two-digit octals.
    self.assertFalse(m.clone().accepts('\\91'))
    self.assertFalse(m.clone().accepts('\\81'))
    self.assertFalse(m.clone().accepts('\\18'))
    self.assertFalse(m.clone().accepts('\\19'))

    # Test invalid three-digit octals.
    self.assertFalse(m.clone().accepts('\\400'))
    self.assertFalse(m.clone().accepts('\\500'))
    self.assertFalse(m.clone().accepts('\\192'))
    self.assertFalse(m.clone().accepts('\\488'))
