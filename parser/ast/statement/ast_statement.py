import parser.ast.ast_expression as ast_expression
import parser.ast.ast_node as ast_node

class ASTStatement(ast_node.ASTNode):

  def __init__(self):
    super(ASTStatement, self).__init__()
    self.expr_type = None

    # A tuple for (In, Out) for the reachability of this node.
    self.reachability = (None, None)

  @staticmethod
  def get_statement(tree):
    '''Return an AST node that is one of:
    ASTIf, ASTWhile, ASTFor, ASTReturn, None
    from a 'Statement', 'StatementWithoutTrailingSubstatement', or
    'StatementNoShortIf' TreeNode'''

    import ast_block
    import ast_for
    import ast_if
    import ast_return
    import ast_while

    child = tree.children[0]

    if tree.value == 'Statement':
      if child.value == 'StatementWithoutTrailingSubstatement':
        return ASTStatement.get_statement(child)
      elif (child.value == 'IfThenStatement' or
            child.value == 'IfThenElseStatement'):
        return ast_if.ASTIf(child)
      elif child.value == 'WhileStatement':
        return ast_while.ASTWhile(child)
      elif child.value == 'ForStatement':
        return ast_for.ASTFor(child)
      else:
        raise ASTStatementError('Statement has unknown child: ' + child.value)

    elif tree.value == 'StatementNoShortIf':
      if child.value == 'StatementWithoutTrailingSubstatement':
        return ASTStatement.get_statement(child)
      elif child.value == 'IfThenElseStatementNoShortIf':
        return ast_if.ASTIf(child)
      elif child.value == 'WhileStatementNoShortIf':
        return ast_while.ASTWhile(child)
      elif child.value == 'ForStatementNoShortIf':
        return ast_for.ASTFor(child)
      else:
        raise ASTStatementError('Statement has unknown child')

    elif tree.value == 'StatementWithoutTrailingSubstatement':
      if child.value == 'Block':
        return ast_block.ASTBlock(child)
      elif child.value == 'EmptyStatement':
        return None
      elif child.value == 'ExpressionStatement':
        return ast_expression.ASTExpression.get_expr_node(child.children[0])
      elif child.value == 'ReturnStatement':
        return ast_return.ASTReturn(child)
      else:
        raise ASTStatementError('Statement has unknown child')

    else:
      raise ASTStatementError('Got a non-statement tree node')

  @property
  def expressions(self):
    # Used to match ASTExpression interface
    return []

class ASTStatementError(Exception):
  pass
