import composed_dfa
import concat
import octal_digit
import one_of
import string_dfa
import zero_to_three

class EscapeSequence(composed_dfa.ComposedDFA):
  '''DFA for recognizing escape sequences'''

  def __init__(self):
    escape_seqs = ['\\b', '\\t', '\\n', '\\f', '\\r', '\\"', "\\'", '\\\\']

    octal = octal_digit.OctalDigit()
    escape_mach = [string_dfa.String(x) for x in escape_seqs]
    escape_mach.extend([
        concat.Concat(string_dfa.String('\\'), octal.clone()),
        concat.Concat(
          concat.Concat(string_dfa.String('\\'), octal.clone()),
          octal.clone()),
        concat.Concat(
          concat.Concat(
            concat.Concat(
              string_dfa.String('\\'), zero_to_three.ZeroToThree()),
            octal.clone()),
          octal.clone())])

    self.machine = one_of.OneOf(*escape_mach)

    # NOTE: This must be called last as self.machine must be set.
    super(EscapeSequence, self).__init__()
