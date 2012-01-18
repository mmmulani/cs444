from composed_dfa import ComposedDFA
from concat import Concat
from floating_point_components import Digits, ExponentPart, FloatTypeSuffix
from one_of import OneOf
from optional import Optional
from string_dfa import String

class FloatingPointLiteral(ComposedDFA):
  def __init__(self):
    machines = []

    # each machine corresponds to a rule for FloatingPointLiteral in the spec
    machines.append(Concat(Digits(), String("."), Optional(Digits()), 
                           Optional(ExponentPart()), 
                           Optional(FloatTypeSuffix())))
    
    machines.append(Concat(String("."), Digits(), Optional(ExponentPart()), 
                           Optional(FloatTypeSuffix())))
    
    machines.append(Concat(Digits(), ExponentPart(), 
                           Optional(FloatTypeSuffix())))
    
    machines.append(Concat(Digits(), Optional(ExponentPart()), 
                           FloatTypeSuffix()))

    self.machine = OneOf(*machines)

    # NOTE: This must be called last as self.machine must be set.
    super(FloatingPointLiteral, self).__init__()
