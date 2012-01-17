from ..one_of_chars import OneOfChars

import unittest
import string

class OneOfCharsTest(unittest.TestCase):

  def test_numbers(self):
    '''Test digits (0-9) in OneOfChars'''
    digits = '0123456789'
    machine = OneOfChars(list(digits))

    for x in digits:
      self.assertTrue(machine.clone().accepts(x))

    for x in string.ascii_uppercase:
      self.assertFalse(machine.clone().accepts(x))

  def test_repeat_args(self):
    '''Test passing duplicated args to OneOfChars'''
    str_input = list('122')
    machine = OneOfChars(str_input)
    for x in str_input:
      self.assertTrue(machine.clone().accepts(x))

    for x in '345':
      self.assertFalse(machine.clone().accepts(x))

  def test_multiple_chars(self):
    '''Test input of multiple characters to OneOfChars'''
    machine = OneOfChars(list(string.ascii_uppercase))

    self.assertTrue(machine.clone().accepts('M'))
    self.assertTrue(machine.clone().accepts('A'))

    self.assertFalse(machine.clone().accepts('MA'))

  def test_ascii_seqs(self):
    '''Test passing weird ASCII sequences to OneOfChars'''
    seqs = [
      [x for x in range(0, 128) if x % 2 == 0],
      [x for x in range(0, 128) if x % 2 == 1],
      [x^2 for x in range(0, 128) if x^2 < 128]
    ]

    for seq in seqs:
      m = OneOfChars([chr(x) for x in seq])
      for x in seq:
        self.assertTrue(m.clone().accepts(chr(x)))
      for x in set(range(0, 128)) - set(seq):
        self.assertFalse(m.clone().accepts(chr(x)))


