import ast_node
import ast_type

class ASTImportList(ast_node.ASTNode):
  @staticmethod
  def get_import_list(tree):
    '''Creates an list of ASTImport from an 'ImportDeclarations' TreeNode'''
    imports = ASTImportList._get_import_list(tree)
    return [ASTImport(imp) for imp in imports]

  @staticmethod
  def _get_import_list(tree):
    imports = []
    while len(tree.children) > 1:
      imports.append(tree.children[1])
      tree = tree.children[0]
    imports.append(tree.children[0])
    imports.reverse()
    return imports

class ASTImport(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an Import AST from an 'ImportDeclaration' TreeNode'''
    # Two children:
    #   0. An AST Type node
    #   1. A bool, indicating whether the import is 'On Demand'

    # TODO (gnleece) does it really make sense for this to be an ASTType?
    type_node = ast_type.ASTType(tree.children[0].children[1])

    # On-Demand imports have 5 children because they have ". *"
    # after the identifiers list:
    is_on_demand = (len(tree.children[0].children) > 3)

    self.children = [type_node, is_on_demand]

  def show(self, depth = 0):
    text = 'Name: {0} - On-demand: {1}'.format(
        '.'.join(self.children[0].children[0].children), str(self.children[1]))
    ast_node.ASTUtils.println(text, depth)

  @property
  def name(self):
    return str(self.children[0])
