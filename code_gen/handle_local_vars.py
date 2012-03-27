from parser.ast.ast_class import ASTClass
from parser.ast.ast_method import ASTMethod
from parser.ast.ast_node import ASTNode
from parser.ast.ast_variable_declaration import ASTVariableDeclaration

def handle_local_vars(asts):
  '''This function takes an array of ASTRoots and annotates any methods with
  information about local variable declarations.
  In particular, it annotates the method with the number of variable
  declarations and annotates each variable declaration with an index into its
  method's stack frame.'''
  for class_ in [ast.class_or_interface for ast in asts if
      ast.class_or_interface and isinstance(ast.class_or_interface, ASTClass)]:
    for m in class_.methods:
      handle_method(m)

def handle_method(ast):
  if ast.body is None:
    return

  # Get all variable declarations in the body.
  var_decls = find_var_decls(ast)

  ast.c_num_local_vars = len(var_decls)

  for ix, decl in enumerate(var_decls):
    decl.c_parent_method = ast
    decl.c_method_frame_index = ix

def find_var_decls(ast):
  decls = []
  for x in ast.children:
    if isinstance(x, ASTVariableDeclaration):
      decls.append(x)
    elif isinstance(x, ASTNode):
      decls.extend(find_var_decls(x))
  return decls
