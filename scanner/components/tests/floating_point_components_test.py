import unittest

from .. import floating_point_components

class FloatingPointComponentsTest(unittest.TestCase):
  def test_digits(self):
    '''Test digits for floating point literal'''
    m = floating_point_components.Digits()
    self.assertTrue(m.clone().accepts("0"))
    self.assertTrue(m.clone().accepts("123"))
    self.assertTrue(m.clone().accepts("0123"))
    self.assertTrue(m.clone().accepts("9876543210"))
    
    self.assertFalse(m.clone().accepts(""))
    self.assertFalse(m.clone().accepts("1.2"))
  
  def test_float_type_suffix(self):
    '''Test float-type-suffixes'''
    m = floating_point_components.FloatTypeSuffix()
    self.assertTrue(m.clone().accepts("f"))
    self.assertTrue(m.clone().accepts("F"))
    self.assertTrue(m.clone().accepts("d"))
    self.assertTrue(m.clone().accepts("D"))
 
    self.assertFalse(m.clone().accepts("a"))
    self.assertFalse(m.clone().accepts("fff"))
    self.assertFalse(m.clone().accepts("fd"))
  
  def test_signed_integer(self):
    '''Test signed integer part of floating point literal'''
    m = floating_point_components.SignedInteger()
    self.assertTrue(m.clone().accepts("1"))
    self.assertTrue(m.clone().accepts("0123"))
    self.assertTrue(m.clone().accepts("+456"))
    self.assertTrue(m.clone().accepts("-456"))
    self.assertTrue(m.clone().accepts("+0"))
    self.assertTrue(m.clone().accepts("-1"))

    self.assertFalse(m.clone().accepts("+"))
    self.assertFalse(m.clone().accepts("-"))
    self.assertFalse(m.clone().accepts("+-123"))
    self.assertFalse(m.clone().accepts("123.45"))
    self.assertFalse(m.clone().accepts("1234+"))

  def test_exponent_part(self):
    '''Test exponent part of floating point literal'''
    m = floating_point_components.ExponentPart()
    self.assertTrue(m.clone().accepts("e+1"))
    self.assertTrue(m.clone().accepts("E+1"))
    self.assertTrue(m.clone().accepts("e123"))
    self.assertTrue(m.clone().accepts("e-123456"))
    
    self.assertFalse(m.clone().accepts("e"))
    self.assertFalse(m.clone().accepts("E"))
    self.assertFalse(m.clone().accepts("+123"))
    self.assertFalse(m.clone().accepts("1337"))
    self.assertFalse(m.clone().accepts("a+1"))
