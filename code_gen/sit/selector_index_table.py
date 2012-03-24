from code_gen.manager import CodeGenManager
from parser.ast.ast_interface import ASTInterface
from parser.ast.ast_class import ASTClass

def make_sit(asts):
  # Determine all interfaces and classes.
  classes = []
  interfaces = []
  for ast in [ast for ast in asts if ast.class_or_interface is not None]:
    if isinstance(ast.class_or_interface, ASTClass):
      classes.append(ast.class_or_interface)
    else:
      interfaces.append(ast.class_or_interface)

  method_selectors = get_selectors(interfaces)

  # Assign an index to each method selector.
  indexed_selectors = zip(range(len(method_selectors)), method_selectors)

  for class_ in classes:
    class_.c_sit_column = create_sit_column(indexed_selectors, class_)

  # Store the column guide on the CodeGenManager so it can do lookups.
  CodeGenManager._sit_column_guide = indexed_selectors

'''get_selectors() returns a list of unique method selectors from all the
interfaces provided.
A selector is a 2-tuple where:
  1. Method return type.
  2. Method signature, a 2-tuple of (name, tuple of parameter types).'''
def get_selectors(interfaces):
  method_selectors = []
  for interface in interfaces:
    methods = interface.methods
    for method in [m for m in methods if not m.is_constructor]:
      selector = (method.return_type, method.signature)

      if not selector in method_selectors:
        method_selectors.append(selector)

  return method_selectors

'''create_sit_column() returns a list representing the SIT column for class_.
Each item in the list is an ASTMethod or None (if the selector was not found on
any of the class' methods).'''
def create_sit_column(indexed_selectors, class_):
  methods = class_.methods
  column = map(lambda(x): None, indexed_selectors)
  class_env = class_.environment
  for ix, (ret, sig) in indexed_selectors:
    (method, _) = class_env.lookup_method(sig)
    if method is None or method.return_type != ret:
      continue

    column[ix] = method

  return column
