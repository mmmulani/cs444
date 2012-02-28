from components.dfa import DFA

class Keyword(DFA):

  KEYWORDS = set([
      "abstract",
      "boolean",
      "break",
      "byte",
      "case",
      "catch",
      "char",
      "class",
      "const",
      "continue",
      "default",
      "do",
      "double",
      "else",
      "extends",
      "final",
      "finally",
      "float",
      "for",
      "goto",
      "if",
      "implements",
      "import",
      "instanceof",
      "int",
      "interface",
      "long",
      "native",
      "new",
      "package",
      "private",
      "protected",
      "public",
      "return",
      "short",
      "static",
      "strictfp",
      "super",
      "switch",
      "synchronized",
      "this",
      "throw",
      "throws",
      "transient",
      "try",
      "void",
      "volatile",
      "while",
  ])

  PREFIXES = set([x[:i] for x in KEYWORDS for i in range(1, len(x) + 1)])

  def __init__(self):
    super(Keyword, self).__init__()

  def _delta(self, x):
    new_lex = self.lexeme + x
    return new_lex in self.PREFIXES

  def is_final(self):
    return self.lexeme in self.KEYWORDS

  def clone(self):
    return Keyword()
