import composed_dfa
import char_range
import one_of

class JavaLetter(composed_dfa.ComposedDFA):
  """ Recognizes the "Java letter" characters, which are
      the uppercase letters (A-Z), lowercase letters (a-z),
      underscore (_) and dollar sign ($)
  """
  def __init__(self):
    self.machine = one_of.OneOf(
        char_range.CharRange(65, 90),
        char_range.CharRange(97, 122),
        char_range.CharRange(36, 36),
        char_range.CharRange(95, 95))

    super(JavaLetter, self).__init__()
