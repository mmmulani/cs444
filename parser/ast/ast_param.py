import ast_node
import ast_type

class ASTParam(ast_node.ASTNode):
  def __init__(self, tree):
    if tree.value != 'FormalParameter':
      raise ASTParamError('Invalid input into ASTParam')

    # FormalParameter Type Identifier
    self.type = ast_type.ASTType(tree.children[0])
    self.name = tree.children[1].value

  def show(self, depth = 0):
    self.type.show()
    ast_node.ASTUtils.println('{0} - {1}'.format(self.type, self.name), depth)

class ASTParamError(Exception):
  pass
