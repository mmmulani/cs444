from .. import null_literal 

import unittest

class NullLiteralTest(unittest.TestCase):
  def test_null(self):
    '''Test null literal'''
    m = null_literal.NullLiteral()
    self.assertTrue(m.delta('n'))
    self.assertTrue(m.delta('u'))
    self.assertTrue(m.delta('l'))
    self.assertTrue(m.delta('l'))
    self.assertTrue(m.is_final())
    self.assertEqual('null', m.lexeme)

    self.assertTrue(m.clone().accepts('null'))
  
  def test_null_casing(self):
    '''Test various casings of null literal.'''
    m = null_literal.NullLiteral()
    self.assertFalse(m.clone().accepts('Null'))
    self.assertFalse(m.clone().accepts('NuLL'))
    self.assertFalse(m.clone().accepts('nulL'))
    self.assertFalse(m.clone().accepts('NULL'))
