import composed_dfa
import one_of
import one_of_chars

class JavaLetter(composed_dfa.ComposedDFA):
  """ Recognizes the "Java letter" characters, which are
      the uppercase letters (A-Z), lowercase letters (a-z),
      underscore (_) and dollar sign ($)
  """
  def __init__(self):
    self.machine = one_of_chars.OneOfChars(
      list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_$'))

    super(JavaLetter, self).__init__()
