import ast_node

class ASTImportList(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an ImportList AST from an 'ImportDeclarations' TreeNode'''
    # 0-N children, each of which are an ASTImport node
    imports = self._get_import_list(tree)
    self.children = [ASTImport(imp) for imp in imports]

  def _get_import_list(self, tree):
    imports = []
    while len(tree.children) > 1:
      imports.append(tree.children[1])
      tree = tree.children[0]
    imports.append(tree.children[0])
    imports.reverse()
    return imports

  def show(self, depth = 0):
    ast_node.ASTUtils.println('Imports:', depth)
    for c in self.children:
      c.show(depth + 1)

class ASTImport(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an Import AST from an 'ImportDeclaration' TreeNode'''
    # Two children:
    #   0. A list of identifiers
    #   1. A bool, indicating whether the import is 'On Demand'

    ids = ast_node.ASTUtils.get_ids_list(tree.children[0].children[1])

    # On-Demand imports have 5 children because they have ". *"
    # after the identifiers list:
    is_on_demand = (len(tree.children[0].children) > 3)

    self.children = [ids, is_on_demand]

  def show(self, depth = 0):
    text = str(self.children[0]) + ', ' + str(self.children[1])
    ast_node.ASTUtils.println(text, depth)
