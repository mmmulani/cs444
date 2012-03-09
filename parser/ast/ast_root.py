import ast_class
import ast_import
import ast_interface
import ast_node
import ast_package

class ASTRoot(ast_node.ASTNode):
  '''The root of an AST Tree'''
  def __init__(self, tree):
    '''Creates an AST Root node from the CompilationUnit state'''
    package = self._get_package_decl(tree)

    # Three children:
    #   0. The package declaration, if any.
    #   1. A list of imports, if any.
    #   2. A class or interface definition, if any.
    # XXX: We must set the package name before calling
    # _get_class_or_interface since the ASTClass will need this information.
    self.children = [package, [], None]
    self.children[1] = self._get_imports(tree)
    self.children[2] = self._get_class_or_interface(tree)

  @property
  def class_or_interface(self):
    return self.children[2]

  @property
  def imports(self):
    return self.children[1]

  @property
  def package(self):
    return self.children[0]

  def show(self, depth = 0, types = False):
    # Package declaration.
    if self.children[0]:
      ast_node.ASTUtils.println(
          'Package declaration: {0}'.format(self.children[0]), depth)

    if len(self.children[1]) > 0:
      ast_node.ASTUtils.println('Imports:', depth)
      for c in self.children[1]:
        c.show(depth + 1, types)

    if self.children[2]:
      ast_node.ASTUtils.println('Declaration:', depth)
      self.children[2].show(depth + 1, types)

  def _get_package_decl(self, tree):
    if tree.length == 0 or tree.children[0].value != 'PackageDeclaration':
      return None
    return ast_package.ASTPackage(tree.children[0])

  def _get_imports(self, tree):
    node = None
    if tree.length > 0 and tree.children[0].value == 'ImportDeclarations':
      node = tree.children[0]
    elif tree.length > 1 and tree.children[1].value == 'ImportDeclarations':
      node = tree.children[1]
    else:
      return []

    return ast_import.ASTImportList.get_import_list(node)

  def _get_class_or_interface(self, tree):
    node = None
    if tree.length > 0 and tree.children[0].value == 'TypeDeclaration':
      node = tree.children[0]
    elif tree.length > 1 and tree.children[1].value == 'TypeDeclaration':
      node = tree.children[1]
    elif tree.length > 2 and tree.children[2].value == 'TypeDeclaration':
      node = tree.children[2]
    else:
      return None

    package_name = ''
    if self.package:
      package_name = str(self.package)

    node = node.children[0]
    if node.value == ';':
      return None
    elif node.value == 'ClassDeclaration':
      return ast_class.ASTClass(node, package_name)
    elif node.value == 'InterfaceDeclaration':
      return ast_interface.ASTInterface(node, package_name)
