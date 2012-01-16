from components.composed_dfa import ComposedDFA
from components.one_of import OneOf
from components.string_dfa import String

class Keyword(ComposedDFA):

  KEYWORDS = [
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
  ]

  def __init__(self):
    machine_list = [String(x) for x in Keyword.KEYWORDS]
    self.machine = OneOf(*machine_list)
    super(Keyword, self).__init__()
