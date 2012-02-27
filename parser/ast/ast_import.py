import ast_expression
import ast_node

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
    #   0. An AST Identifiers node
    #   1. A bool, indicating whether the import is 'On Demand'

    ids = ast_expression.ASTIdentifiers(tree.children[0].children[1])

    # On-Demand imports have 5 children because they have ". *"
    # after the identifiers list:
    is_on_demand = (len(tree.children[0].children) > 3)

    self.children = [ids, is_on_demand]

  def show(self, depth = 0):
    text = 'Name: {0} - On-demand: {1}'.format(
        '.'.join(self.children[0].children), str(self.children[1]))
    ast_node.ASTUtils.println(text, depth)

  @property
  def name(self):
    return str(self.children[0])

  @property
  def on_demand(self):
    return self.children[1]
