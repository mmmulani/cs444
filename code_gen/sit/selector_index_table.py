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

def get_selectors(interfaces):
  '''get_selectors() returns a list of unique method selectors from all the
  interfaces provided.
  A selector is a 2-tuple where:
    1. Method return type.
    2. Method signature, a 2-tuple of (name, tuple of parameter types).'''
  method_selectors = []
  for interface in interfaces:
    methods = interface.methods
    for method in [m for m in methods if not m.is_constructor]:
      selector = (method.return_type, method.signature)

      if not selector in method_selectors:
        method_selectors.append(selector)

  return method_selectors

def create_sit_column(indexed_selectors, class_):
  '''create_sit_column() returns a list representing the SIT column for class_.
  Each item in the list is an ASTMethod or None (if the selector was not found on
  any of the class' methods).'''
  methods = class_.methods
  column = map(lambda(x): None, indexed_selectors)
  class_env = class_.environment
  for ix, (ret, sig) in indexed_selectors:
    (method, _) = class_env.lookup_method(sig)
    if method is None or method.return_type != ret:
      continue

    column[ix] = method

  return column

def gen_code_sit_column(sit_column, label):
  '''Generates assembly for the SIT table for this type.'''
  table_entries = []
  for ix, m in enumerate(sit_column):
    # Add an assembly comment to explain the row.
    selector = CodeGenManager.get_selector(ix)
    ret_type, (name, params) = selector
    param_strs = [str(t) for t in params]
    method_str = '{0} {1}({2})'.format(str(ret_type), name,
        ', '.join(param_strs))
    table_entries.append('; {0}'.format(method_str))

    entry = ''
    if m is None:
      entry = 'dd 0x0'
    else:
      entry = 'dd {0}'.format(m.c_defn_label)

    table_entries.append(entry)

  return [
      'global {0}'.format(label),
      '{0}:'.format(label),
      table_entries
  ]
