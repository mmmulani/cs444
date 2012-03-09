import types

import parser.ast.ast_expression as ast_expression
import parser.ast.ast_type as ast_type
import rules

# get a list of all the type-checking rules:
rule_funcs = [rules.__dict__.get(x) for x in dir(rules) if
    isinstance(rules.__dict__.get(x), types.FunctionType) and x[0] != '_']

_global_params = {
  'cur_method': None,
  'cur_class': None
}

def set_params(param_dict):
  clear_params()
  for param in param_dict:
    if param in _global_params:
      _global_params[param] = param_dict[param]

def get_param(key):
  return _global_params[key]

def clear_params():
  '''Clear the global paramaters for re-use'''
  for key in _global_params.keys():
    _global_params[key] = None

def check_types(ast):
  '''Takes an AST for a file and type-checks its class/interface'''

  # the class or interface definition:
  decl = ast.children[2]
  # type check all fields and methods:
  if decl:
    for method in decl.methods:
      set_params({
        'cur_method': method,
        'cur_class': decl
      })
      get_type(method.body)
      clear_params()
    for field in decl.fields:
      get_type(field)

def get_type(ast):
  '''Tries to assign a type to the given AST by applying all the type checking
  rules. Exactly one rule should apply to an AST, so an exception is thrown if
  zero or multiple rules apply.'''

  if ast is None:
    return None #TODO (gnleece) what should really happen here?

  # check if the type has already been set:
  if ast.expr_type:
    return ast.expr_type

  # try all possible rules:
  possible_types = filter(None, [rule(ast) for rule in rule_funcs])

  # TODO (gnleece) uncomment this when type checking is fully written
  #if len(possible_types) == 0:
  #  raise TypeCheckingError('Expression could not be typed')
  if len(possible_types) > 1:
    raise TypeCheckingError('Expression has multiple possible types')

  if len(possible_types) == 0:
    raise TypeCheckingError('Expression has no type')

  ast.expr_type = possible_types[0]
  return possible_types[0]

class TypeCheckingError(Exception):
  def __init__(self, msg):
    self.msg = msg
