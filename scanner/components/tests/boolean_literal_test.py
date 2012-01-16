from .. import boolean_literal

import unittest

class BooleanLiteralTest(unittest.TestCase):
  def test_boolean(self):
    '''Test boolean literals'''
    m = boolean_literal.BooleanLiteral()

    self.assertTrue(m.clone().accepts('true'))
    self.assertTrue(m.clone().accepts('false'))

  def test_boolean_casing(self):
    '''Test various casing of booleans'''
    m = boolean_literal.BooleanLiteral()

    self.assertFalse(m.clone().accepts('True'))
    self.assertFalse(m.clone().accepts('tRue'))
    self.assertFalse(m.clone().accepts('TrUe'))
    self.assertFalse(m.clone().accepts('TRUE'))

    self.assertFalse(m.clone().accepts('False'))
    self.assertFalse(m.clone().accepts('fAlse'))
    self.assertFalse(m.clone().accepts('FalsE'))
    self.assertFalse(m.clone().accepts('FALSE'))

  def test_combined_boolean(self):
    '''Test mixing booleans together'''
    m = boolean_literal.BooleanLiteral()

    self.assertFalse(m.clone().accepts('trlse'))
    self.assertFalse(m.clone().accepts('faue'))
