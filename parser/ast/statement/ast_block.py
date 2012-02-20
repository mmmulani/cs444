import parser.ast.ast_node as ast_node
import ast_statement

class ASTBlock(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST block node from a 'Block' TreeNode'''

    # Each child is a LocalVariableDeclaration, Statement, or ClassDeclration
    self.children = []

    if len(tree.children) == 2:
      return

    statements = tree.children[1]
    stmt_list = []
    while len(statements.children) == 2:
      stmt_list.append(statements.children[1].children[0])
      statements = statements.children[0]
    stmt_list.append(statements.children[0].children[0])

    for stmt in stmt_list:
      if stmt.value == 'Statement':
        self.children.append(ast_statement.ASTStatement.get_statement(stmt))
      elif stmt.value == 'LocalVariableDeclarationStatement':
      # TODO (gnleece) uncomment when Local Var Decls are done
      #  self.children.append(ASTLocalVariableDeclaration(stmt))
        pass
      else:
        raise ASTBlockError('Block treenode has invalid children')

class ASTBlockError(Exception):
  pass

