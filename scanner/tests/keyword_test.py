import unittest

from ..keyword import Keyword

class TestKeyword(unittest.TestCase):
  def setUp(self):
    self.machine = Keyword()

  def test_all_keywords(self):
    for kw in Keyword.KEYWORDS:
      self.assertTrue(self.machine.clone().accepts(kw))

  def test_non_keywords(self):
    self.assertFalse(self.machine.clone().accepts("foo"))
    self.assertFalse(self.machine.clone().accepts("abstract_foo"))

if __name__ == '__main__':
  unittest.main()
