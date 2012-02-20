import ast_node

class ASTVariableDeclaration(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Variable Declaration node from a 'FieldDeclaration'
    or a 'LocalVariableDeclaration' TreeNode'''
    # Four children:
    #   0. A set of modifiers
    #   1. A Type AST node
    #   2. An identifier
    #   3. An expression, or None

    modifiers = set()
    if tree.children[0].value == 'Modifiers':
      modifiers = ast_node.ASTUtils.get_modifiers_set(tree.children[0])
      type_node = tree.children[1]
      declarator_node = tree.children[2]
    else:
      type_node = tree.children[0]
      declarator_node = tree.children[1]

    type_ast = ASTType(type_node)

    identifier = declarator_node.children[0]

    expression_ast = None
    # TODO (gnleece) uncomment when expressions are done
    #if len(declarator_node.children) > 1):
    #  expression_ast = ASTExpression(declarator_node.children[2])

    self.children = [modifiers, type_ast, identifier, expression_ast]
