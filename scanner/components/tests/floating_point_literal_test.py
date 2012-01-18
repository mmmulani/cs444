import unittest

from ..floating_point_literal import FloatingPointLiteral

class FloatingPointLiteralTest(unittest.TestCase):
  def test_valid_floats(self):
    '''Test valid floating point literals'''
    m = FloatingPointLiteral()
    
    # examples from Java spec:
    self.assertTrue(m.clone().accepts("1e1f"))
    self.assertTrue(m.clone().accepts("2.f"))
    self.assertTrue(m.clone().accepts(".3f"))
    self.assertTrue(m.clone().accepts("0f"))
    self.assertTrue(m.clone().accepts("3.14f"))
    self.assertTrue(m.clone().accepts("6.022137e+23f"))
    self.assertTrue(m.clone().accepts("1e1"))
    self.assertTrue(m.clone().accepts("2."))
    self.assertTrue(m.clone().accepts(".3"))
    self.assertTrue(m.clone().accepts("0.0"))
    self.assertTrue(m.clone().accepts("3.14"))
    self.assertTrue(m.clone().accepts("1e-9d"))
    self.assertTrue(m.clone().accepts("1e137"))

    self.assertTrue(m.clone().accepts("0.123d"))
    self.assertTrue(m.clone().accepts("0.123f"))
    self.assertTrue(m.clone().accepts("0.123D"))
    self.assertTrue(m.clone().accepts("0.123F"))
    self.assertTrue(m.clone().accepts("0.123"))
    self.assertTrue(m.clone().accepts("111.e6"))
    self.assertTrue(m.clone().accepts("111.e+6f"))
    self.assertTrue(m.clone().accepts(".3e+6"))
    self.assertTrue(m.clone().accepts(".3e-6f"))
    self.assertTrue(m.clone().accepts(".3d"))

  def test_invalid_floats(self):
    '''Test invalid floating point literals'''

    m = FloatingPointLiteral()

    self.assertFalse(m.clone().accepts("123"))
    self.assertFalse(m.clone().accepts(".e"))
    self.assertFalse(m.clone().accepts(".e+1"))
    self.assertFalse(m.clone().accepts("123.f+e6"))
    self.assertFalse(m.clone().accepts("1337fe10"))
    self.assertFalse(m.clone().accepts("f"))
    self.assertFalse(m.clone().accepts("e+1"))
    self.assertFalse(m.clone().accepts("123.456."))
