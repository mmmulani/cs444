import parser.ast.ast_node as ast_node
import ast_statement

class ASTFor(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST For node from a 'ForStatement' or
    'ForStatementNoShortIf' TreeNode'''
    # Four children:
    #   0. ???, or None
    #   1. An expression, or None
    #   2. ???, or None
    #   3. A statement

    for_init = None
    expression = None
    for_update = None
    statement = None

    for child in tree.children:
      #if child.value == 'ForInit':
      #  for_init = child
      #elif child.value == 'Expression':
      #  expression = ASTExpression(child)
      #elif child.value == 'ForUpdate':
      #  for_update = child
      if child.value == 'Statement':
        statement = ast_statement.ASTStatement.get_statement(child)

    if statement is None:
      raise ASTForError('For treenode must have a statement')

    self.children = [for_init, expression, for_update, statement]

class ASTForError(Exception):
  pass
