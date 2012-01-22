from components.boolean_literal import BooleanLiteral
from components.character_literal import CharacterLiteral
from components.composed_dfa import ComposedDFA
from components.floating_point_literal import FloatingPointLiteral
from components.integer_literal import IntegerLiteral
from components.null_literal import NullLiteral
from components.one_of import OneOf
from components.string_literal import StringLiteral

class Literal(ComposedDFA):

  def __init__(self):
    self.machine = OneOf(IntegerLiteral(), FloatingPointLiteral(), 
                         BooleanLiteral(), CharacterLiteral(), 
                         StringLiteral(), NullLiteral())
    super(Literal, self).__init__()
