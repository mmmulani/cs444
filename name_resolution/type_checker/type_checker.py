import types

import parser.ast.ast_expression as ast_expression
import rules

def check_types(ast):
  '''Takes an AST for a file and type-checks its class/interface'''

  # get a list of all the type-checking rules:
  rule_funcs = [rules.__dict__.get(x) for x in dir(rules) if
      isinstance(rules.__dict__.get(x), types.FunctionType)]

  # the class or interface definition:
  decl = ast.children[2]
  # type check all fields and methods:
  if decl:
    for method in decl.methods:
      type_check_node(method, rule_funcs)
    for field in decl.fields:
      type_check_node(field, rule_funcs)


def type_check_node(ast, rule_funcs):
  '''Tries to assign a type to the given AST by applying all the type checking
  rules. Exactly one rule should apply to an AST, so an exception is thrown if
  zero or multiple rules apply.'''

  # try all possible rules:
  possible_types = filter(None, [rule(ast) for rule in rule_funcs])

  if len(possible_types) == 0:
    raise TypeCheckingError('Expression could not be typed')
  elif len(possible_types) > 1:
    raise TypeCheckingError('Expression has multiple possible types')

  ast.expr_type = possible_types[0]
  return possible_types[0]


class TypeCheckingError(Exception):
  pass
