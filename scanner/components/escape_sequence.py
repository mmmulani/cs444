import one_of_chars
import composed_dfa
import concat
import octal_digit
import one_of
import string_dfa

class ZeroToThree(composed_dfa.ComposedDFA):
  '''Recognizes the digits 0, 1, 2, 3'''

  def __init__(self):
    self.machine = one_of_chars.OneOfChars(list('0123'))

    # NOTE: This must be called last as self.machine must be set.
    super(ZeroToThree, self).__init__()

class EscapeSequence(composed_dfa.ComposedDFA):
  '''DFA for recognizing escape sequences'''

  def __init__(self):
    escape_seqs = ['\\b', '\\t', '\\n', '\\f', '\\r', '\\"', "\\'", '\\\\']

    octal = octal_digit.OctalDigit()
    escape_mach = [string_dfa.String(x) for x in escape_seqs]
    escape_mach.extend([
        concat.Concat(string_dfa.String('\\'), octal.clone()),
        concat.Concat(
          string_dfa.String('\\'), octal.clone(), octal.clone()),
        concat.Concat(
          string_dfa.String('\\'), ZeroToThree(), octal.clone(), octal.clone())
      ])

    self.machine = one_of.OneOf(*escape_mach)

    # NOTE: This must be called last as self.machine must be set.
    super(EscapeSequence, self).__init__()
