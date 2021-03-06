import ast_statement
import parser.ast.ast_node as ast_node
import parser.ast.ast_variable_declaration as ast_variable_declaration
from parser.ast.ast_node import ASTUtils

class ASTBlock(ast_statement.ASTStatement):
  def __init__(self, tree):
    '''Creates an AST block node from a 'Block' TreeNode'''
    super(ASTBlock, self).__init__()

    # Each child is a VariableDeclaration or Statement
    # (astnode, is_statement)
    self.children = []

    # This is set by the Environment module when the tree is complete.
    self.environment = None

    # We use this hack to create ASTBlocks without a parse tree in
    # from_statements.
    if tree is None:
      return

    if len(tree.children) == 2:
      return

    statements = tree.children[1]
    stmt_list = []
    while len(statements.children) == 2:
      stmt_list.append(statements.children[1].children[0])
      statements = statements.children[0]
    stmt_list.append(statements.children[0].children[0])

    statements = []
    for stmt in stmt_list:
      if stmt.value == 'Statement':
        new_statement = ast_statement.ASTStatement.get_statement(stmt)
        if new_statement is not None:
          statements.append(ast_statement.ASTStatement.get_statement(stmt))
      elif stmt.value == 'LocalVariableDeclarationStatement':
        statements.append(ast_variable_declaration.ASTVariableDeclaration(
            stmt.children[0]))
      else:
        raise ASTBlockError('Block treenode has invalid children')

    # Reverse the statements so they're in the correct order.
    statements.reverse()

    self.children = self.process_statements(statements)

  @staticmethod
  def from_statements(statements):
    new_block = ASTBlock(None)
    new_block.children = new_block.process_statements(statements)
    return new_block

  def process_statements(self, statements):
    # Check to see if we have two VariableDeclarations in the statements. If we
    # do, wrap the second VariableDeclaration and all statements after it in a
    # new block. This makes determining if a variable has been used before its
    # declaration much easier.

    found_ix = -1
    seen_declaration = False
    for ix, statement in enumerate(statements):
      if type(statement) == ast_variable_declaration.ASTVariableDeclaration:
        if seen_declaration:
          found_ix = ix
          break
        else:
          seen_declaration = True

    if found_ix == -1:
      return statements

    statements_before_decl = statements[:ix]
    statements_with_decl = statements[ix:]

    new_block = ASTBlock.from_statements(statements_with_decl)

    statements_before_decl.append(new_block)

    return statements_before_decl

  @property
  def statements(self):
    return list(self.children)

  @property
  def expressions(self):
    return self.statements

  def show(self, depth = 0, types = False, show_name = False):
    if show_name:
      ASTUtils.println('ASTBlock: {0}'.format(
          ASTUtils.type_string(self.expr_type)), depth)
      depth = depth + 1

    for c in self.children:
      if type(c) == ASTBlock:
        c.show(depth, types, show_name = True)
      else:
        c.show(depth, types)

  # Code generation functions ------------------
  def c_gen_code(self):
    asm = [c.c_gen_code() for c in self.children if c is not None]
    return asm


class ASTBlockError(Exception):
  pass

