import ast_expression
import ast_node
import ast_type

class ASTCast(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Cast node from a 'CastExpression' TreeNode'''

    # Two children.
    #   0. A type node going to the type, and
    #   1. An expression node for the expression

    self.children = [self._create_type_node(tree),
        ast_expression.ASTExpression.get_expr_node(tree.children[-1])]

  def _create_type_node(self, tree):
    type_node = tree.children[1]
    ret = None

    if type_node.value in ['PrimitiveType', 'Identifiers']:
      ret = ast_type.ASTType(type_node)
    elif type_node.value == 'Expression':
      # Expression will have to go to Identifiers eventually, as per the weeder.
      identifiers_node = self._get_identifiers_node(type_node)
      ret = ast_type.ASTType(identifiers_node)
    else:
      # This should never happen
      raise ASTCastError('CastExpression has unknown type')

    # Check if the cast is to an array type.
    if tree.children[2].value == 'Dim':
      ret.is_array = True

    return ret

  def _get_identifiers_node(self, expr_node):
    while expr_node.value != 'Expression':
      expr_node = expr_node.children[0]
    return expr_node

  def show(self, depth):
    ast_node.ASTUtils.println(
        'ASTCast Type: {0}'.format(self.children[0]), depth)
    self.children[1].show(depth + 1)


class ASTCastError(Exception):
  pass
