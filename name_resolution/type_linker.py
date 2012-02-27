import parser.ast.ast_expression as ast_expression
import parser.ast.ast_variable_declaration as ast_variable_declaration
import parser.ast.statement as ast_statement
import parser.ast.ast_class as ast_class
import parser.ast.ast_class as ast_interface

def link_names(ast):
  decl = ast.children[2]
  if decl:
    env = decl.environment
    for super_type in decl.super:
      # Link inherited class / inherited interfaces.
      link(super_type, env)

      # Inheritance checks.

      # Classes can only extend other classes.
      # Interfaces can only extend other interfaces.
      if super_type.definition is not None and \
          is_class(super_type.definition) == is_class(decl):
        raise TypeLinkerError('Extending type mismatch')

      # Classes/Interfaces can not extend themselves.
      if super_type.definition is not None and \
          super_type.definition == decl:
        raise TypeLinkerError('Type is extending itself')

    for inter in decl.interfaces:
      # Link implemented interfaces.
      link(inter, env)

      # Implements checks.

      # Classes can not implement classes.
      if inter.definition is not None and is_class(inter.definition):
        raise TypeLinkerError('Class is implementeting a class')

    for f in decl.fields:
      # Link field types.
      link(f.type_node, env)

    for m in decl.methods:
      # Link method return types and parameters.
      if m.is_constructor:
        pass
      else:
        link(m.return_type, env)

      for p in m.params:
        link(p.type, env)

      if m.children[0]:
        link_block(m.children[0], env)

def link(ast, env):
  '''Actually sets the definition for an ASTType node'''
  if ast is None or ast.is_primitive():
    # Don't need to link primitive types.
    return
  definition = env.lookup(ast.name)
  if definition is None:
    raise TypeLinkerError('Type name not found')
  ast.children[0].definition = definition

def link_variable_declaration(ast, env):
  link(ast.type_node, env)

def link_block(ast, env):
  for x in ast.children:
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
  link_statement(ast.statement, env)

def link_if(ast, env):
  '''Links for ASTIf node'''
  link_expression(ast.expression, env)
  link_statement(ast.if_statement, env)
  if ast.else_statement:
    link_statement(ast.else_statement, env)

def link_cast(ast, env):
  '''Links for ASTCast'''
  link(ast.type_node, env)

def link_expression(ast, env):
  '''Links for one of the possible ASTExpression nodes'''
  t = type(ast)
  if t == ast_expression.ASTCast:
    link_cast(ast, env)
  elif t == ast_expression.ASTInstanceOf:
    link(ast.type_node, env)

  # Recurse for each expression child.
  for e in ast.expressions:
    link_expression(e, env)

def link_statement(ast, env):
  '''Links for one of the possible ASTStatement nodes'''
  # FML.
  t = type(ast)
  if t == ast_statement.ast_block.ASTBlock:
    link_block(ast, env)
  elif t == ast_statement.ast_for.ASTFor:
    link_for(ast, env)
  elif t == ast_statement.ast_return.ASTReturn:
    link_return(ast, env)
  elif t == ast_statement.ast_while.ASTWhile:
    link_while(ast, env)
  elif t == ast_statement.ast_if.ASTIf:
    link_if(ast, env)
  elif t == ast_expression.ASTExpression:
    link_expression(ast, env)

def is_class(ast):
  if type(decl) not in [ast_class.ASTClass, ast_interface.ASTInterface]:
    raise TypeLinkerError(
        'Tried to call is_class() on a non-class/interface object')
  return (type(decl) == ast_class.ASTClass)

class TypeLinkerError(Exception):
  pass
