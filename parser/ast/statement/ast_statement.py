import parser.ast.ast_node as ast_node
import ast_block
import ast_for
import ast_if
import ast_return
import ast_while

class ASTStatement(ast_node.ASTNode):

  @staticmethod
  def get_statement(tree):
    '''Return an AST node that is one of:
    ASTIf, ASTWhile, ASTFor, ASTReturn, None
    from a 'Statement', 'StatementWithoutTrailingSubstatement', or
    'StatementNoShortIf' TreeNode'''

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
        pass
        #TODO (gnleece) add expression here when expressions are done
      elif child.value == 'ReturnStatement':
        return ast_return.ASTReturn(child)
      else:
        raise ASTStatementError('Statement has unknown child')

    else:
      raise ASTStatementError('Got a non-statement tree node')

class ASTStatementError(Exception):
  pass
