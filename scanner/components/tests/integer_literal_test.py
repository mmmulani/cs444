import unittest

from ..integer_literal import IntegerLiteral

class TestIntegerLiteral(unittest.TestCase):
  def setUp(self):
    self.machine = IntegerLiteral()

  def test_integer_literal(self):
    '''Test integer literals'''
    literals = [
      '123',
      '0',
      '123999',
      '123456789',
      '0x5',
      '0x0',
      '0x0000',
      '0x0Aa',
      '0xdeadbeef',
      '0xDeADbEEf0000',
      '0xAAA',
      '0xabcdef01',
      '0x01ABCDEF',
      '00',
      '0001',
      '0123'
    ]
    literals.extend([hex(x) for x in range(0, 16)])

    bad_lits = [
      '09',
      '0xabcg',
      '130.123',
      '1x234',
      '0x0ll'
    ]

    for x in literals:
      for suffix in ['', 'l', 'L']:
        self.assertTrue(self.machine.clone().accepts(x + suffix))

    for x in bad_lits:
      self.assertFalse(self.machine.clone().accepts(x))

if __name__ == '__main__':
  unittest.main()
