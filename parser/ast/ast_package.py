import ast_node

class ASTPackage(ast_node.ASTNode):
  '''Creates a package AST node from a PackageDeclaration node'''
  def __init__(self, tree):
    if tree.value != 'PackageDeclaration':
      raise ASTPackageError('Invalid tree node given to AST Package')

    self._name = ast_node.ASTUtils.get_ids_list(tree.children[1])

    # No children.

  def show(self, depth = 0):
    ast_node.ASTUtils.println(self.name, depth)

  @property
  def name(self):
    return '.'.join(self._name)

class ASTPackageError(Exception):
  pass
