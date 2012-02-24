import ast_node

from ast_expression import ASTIdentifiers

class ASTPackage(ast_node.ASTNode):
  '''Creates a package AST node from a PackageDeclaration node'''
  def __init__(self, tree):
    if tree.value != 'PackageDeclaration':
      raise ASTPackageError('Invalid tree node given to AST Package')

    self._name = ASTIdentifiers(tree.children[1])

    # No children.

  def show(self, depth = 0):
    ast_node.ASTUtils.println(self.name, depth)

  @property
  def name(self):
    return '.'.join(self._name.children)

  def __str__(self):
    return self.name

class ASTPackageError(Exception):
  pass
