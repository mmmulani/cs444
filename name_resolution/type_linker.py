import parser.ast.ast_expression as ast_expression
import parser.ast.ast_variable_declaration as ast_variable_declaration
import parser.ast.statement as ast_statement

def link_names(ast):
  imports = ast.children[1]
  env = ast.environment

  # Import declarations.
  for im in imports:
    link_imports(im, env)

  decl = ast.children[2]
  if decl:
    env = decl.environment
    for super_type in decl.super:
      # Link inherited class / inherited interfaces.
      link(super_type, env)
    for inter in decl.interfaces:
      # Link implemented interfaces.
      link(inter, env)

    for f in decl.fields:
      # Link field types.
      link_type(f.type, env)

    for m in decl.methods:
      # Link method return types and parameters.
      if m.is_constructor:
        pass
      else:
        link_type(m.return_type, env)
      for p in m.params:
        link_type(p.type, env)

      link_block(m.children[0])

def link(ast, env):
  '''Links an ASTIdentifiers node with its definition.'''
  ast.definition = env.lookup(str(ast))

def link_type(ast, env):
  if ast.is_primitive:
    # Don't need to link primitive types.
    return
  ast.children[0].definition = env.lookup(ast.name)

def link_imports(ast, env):
  '''Links imports from one AST to their definitions via the Environment

  Params:
    1. An ASTImport object
    2. A (global) environment for that file
  '''

  # Only single-type-import declarations can be linked syntactically.
  if ast.is_on_demand:
    return
  link(ast.children[0], env)

def link_variable_declaration(ast, env):
  '''Links the type for an ASTVariableDeclaration with its definition'''
  link_type(ast.type_ast, env)

def link_block(ast):
  env = ast.environment
  for x in body.children:
    # Each child of the body is a VariableDeclaration or Statement.
    if type(x) == ast_variable_declaration.ASTVariableDeclaration:
      link_variable_declaration(x, env)
    else:
      link_statement(x, env)

def link_return(ast, env):
  '''Links for ASTReturn node'''
  if ast.children[0]:
    # Link expression node.
    link_expression(ast.children[0], env)

def link_for(ast, env):
  '''Links for ASTFor node'''
  if ast.init:
    # This code makes gnleece cry
    if type(ast.init) == ast_variable_declaration.ASTVariableDeclaration:
      link_variable_declaration(ast.init, env)
    else:
      link_expression(ast.init, env)
  if ast.expression:
    link_expression(ast.expression, env)
  if ast.update:
    link_expression(ast.update, env)
  if ast.statement:
    link_statement(ast.statement, env)

def link_while(ast, env):
  '''Links for ASTWhile node'''
  link_expression(ast.expression, env)
  link_statement(ast.statement, ev)

def link_if(ast, env):
  '''Links for ASTIf node'''
  link_expression(ast.expression, env)
  link_statement(ast.if_statement, env)
  if ast.else_statement:
    link_statement(ast.else_statement, env)

def link_cast(ast, env):
  '''Links for ASTCast'''
  link_type(ast.type_node, env)

def link_expression(ast, env):
  '''Links for one of the possible ASTExpression nodes'''
  t = type(ast)
  if t == ast_expression.ASTCast:
    link_cast(ast, env)
  elif t == ast_expression.ASTBinary:
    # We need to check the type for instanceof here
    pass
  else:
    # We don't need to deal with other types of expressions at this point in
    # time.
    return

def link_statement(ast, env):
  '''Links for one of the possible ASTStatement nodes'''
  # FML.
  t = type(ast)
  if t == ast_statement.ast_block.ASTBlock:
    link_block(ast)
  elif t == ast_statement.ast_for.ASTFor:
    link_for(ast, env)
  elif t == ast_statement.ast_return.ASTReturn:
    link_return(ast, env)
  elif t == ast_statement.ast_while.ASTWhile:
    link_while(ast, env)
  elif t == ast.statement.ast_if.ASTIf:
    link_if(ast, env)
  elif t == ast_expression.ASTExpression:
    link_expression(ast, env)
