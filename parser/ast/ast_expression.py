from ast_node import ASTNode, ASTUtils
from ast_cast import ASTCast
from ast_type import ASTType

class ASTExpression(ASTNode):
  '''General ASTExpression class with a function to create the proper ASTNode'''

  @staticmethod
  def get_expr_node(tree):
    '''
    Given a *Expression node, returns the appropriate ASTNode.
    Can also take a Primary[NoNewArray] node and return the appropriate ASTNode.
    '''

    # TODO(mehdi): Is this Primary case even needed? See if they can fall into
    # the general case.
    # Handle the case where tree is a Primary[NoNewArray] node.
    if tree.value == 'Primary' or tree.value == 'PrimaryNoNewArray':
      # Before going down one node, handle the only case where there are
      # multiple children, the "( Expression )" case.
      if len(tree.children) == 3 and tree.children[0].value == '(':
        return ASTExpression.get_expr_node(tree.children[1])

      child = tree.children[0]
      if child.value == 'ArrayCreationExpression':
        return ASTArrayCreation(child)
      elif child.value == 'PrimaryNoNewArray':
        child = child.children[0]

      if child.value == 'Literal':
        return ASTLiteral(child)
      elif child.value == 'this':
        return ASTThis(child)
      elif child.value == 'ClassInstanceCreationExpression':
        return ASTClassInstanceCreation(child)
      elif child.value == 'FieldAccess':
        return ASTFieldAccess(child)
      elif child.value == 'MethodInvocation':
        return ASTMethodInvocation(child)
      elif child.value == 'ArrayAccess':
        return ASTArrayAccess(child)
      elif child.value == 'Identifiers' or child.value == 'Identifier':
        return ASTIdentifiers(child)

    # Default to the general case where the tree is a long Expression parse tree
    # that widens based on the type of expression.
    child = ASTUtils.get_nonpath_child(tree)

    if child.value == 'Literal':
      return ASTLiteral(child)
    elif (child.value == 'UnaryExpression'
          or child.value == 'UnaryExpressionNotPlusMinus'):
      return ASTUnary(child)
    elif child.value == 'CastExpression':
      return ASTCast(child)
    elif child.value == 'Assignment':
      return ASTAssignment(child)
    elif child.value == 'ArrayAccess':
      return ASTArrayAccess(child)
    elif child.value == 'this':
      return ASTThis(child)
    elif child.value == 'super':
      return ASTSuper(child)
    elif child.value == 'FieldAccess':
      return ASTFieldAccess(child)
    elif child.value == 'MethodInvocation':
      return ASTMethodInvocation(child)
    elif child.value == 'ArrayCreationExpression':
      return ASTArrayCreation(child)
    elif child.value == 'ClassInstanceCreationExpression':
      return ASTClassInstanceCreation(child)
    elif child.value == 'PrimaryNoNewArray':
      return ASTExpression.get_expr_node(child.children[1])
    elif child.value == 'Identifiers' or child.value == 'Identifier':
      return ASTIdentifiers(child)
    else:
      # This should be a Binary expression.
      # TODO(mehdi) add checks
      return ASTBinary(child)

    raise ASTExpressionError('Unhandled Expression')

class ASTExpressionError(Exception):
  pass

class ASTFieldAccess(ASTNode):
  def __init__(self, tree):
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]

class ASTLiteral(ASTNode):
  def __init__(self, tree):
    # TODO: Add typing info and possibly check that the literal is valid Joos.
    self.children = [tree.lexeme]

  def show(self, depth = 0):
    ASTUtils.println(
      'Literal: {0}'.format(self.children[0]), depth)

class ASTUnary(ASTNode):
  def __init__(self, tree):
    # TODO: Convert operator to an enum?
    self.operator = tree.children[0].lexeme
    self.children = [ASTExpression.get_expr_node(tree.children[1])]

  def show(self, depth = 0):
    ASTUtils.println(
      'ASTUnary, operator: {0}'.format(self.operator), depth)
    ASTUtils.println('Operand:', depth)
    self.children[0].show(depth + 1)

class ASTAssignment(ASTNode):
  def __init__(self, tree):
    # tree should be an Assignment node.
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]

class ASTArrayAccess(ASTNode):
  def __init__(self, tree):
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]

class ASTThis(ASTNode):
  def __init__(self, tree):
    self.children = []

class ASTSuper(ASTNode):
  def __init__(self, tree):
    self.children = []

class ASTMethodInvocation(ASTNode):
  def __init__(self, tree):
    self.children = []
    # self.children is of length 2:
    # - first is an array of expressions to be evaluated in order, and then
    #   accessed by field. e.g.:
    #     (i.j).k => [Expression for "(i.j)", Expression for "k"]
    # - second is an array of argument expressions (possibly empty)
    if tree.children[0].value == 'Identifiers':
      self.children.append([ASTExpression.get_expr_node(tree.children[0])])
      if tree.children[2].value == 'ArgumentList':
        self.children.append(ASTUtils.get_arg_list(tree.children[2]))
      else:
        self.children.append([])
    else:
      prefix_exprs = [ASTExpression.get_expr_node(tree.children[0]),
                      ASTExpression.get_expr_node(tree.children[2])]
      if tree.children[4].value == 'ArgumentList':
        arg_list = ASTUtils.get_arg_list(tree.children[4])
      else:
        arg_list = []

      self.children = [prefix_exprs, arg_list]

  def show(self, depth = 0):
    self._show(depth)
    if len(self.children[0]) == 1:
      ASTUtils.println('Method identifiers:')
      self.children[0][0].show(depth + 1)
    else:
      ASTUtils.println('Expression:', depth)
      self.children[0][0].show(depth + 1)
      ASTUtils.println('Field access from expression:', depth)
      self.children[0][1].show(depth + 1)
    for i, x in enumerate(self.children[1]):
      ASTUtils.println('Argument {0}:'.format(str(i)), depth)
      x.show(depth + 1)

class ASTBinary(ASTNode):
  # children is [left operand, right operand]
  def __init__(self, tree):
    # TODO: convert operator to enum?
    self.operator = tree.children[1].lexeme
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]

  def show(self, depth = 0):
    ASTUtils.println('ASTBinary, operator: {0}'.format(self.operator), depth)
    ASTUtils.println('Left operand:', depth)
    self.children[0].show(depth + 1)
    ASTUtils.println('Right operand:', depth)
    self.children[1].show(depth + 1)

class ASTClassInstanceCreation(ASTNode):
  # Children is of length 2:
  # 0. ASTIdentifiers corresponding to class type.
  # 1. List of arguments (possibly empty).
  def __init__(self, tree):
    self.children = [ASTExpression.get_expr_node(tree.children[1])]
    if tree.children[3].value == 'ArgumentList':
      self.children.append(ASTUtils.get_arg_list(tree.children[3]))
    else:
      self.children.append([])

    # Will be set by the type linker.
    self.definiton = None

  def show(self, depth = 0):
    self._show(depth)
    ASTUtils.println('Class type:', depth)
    self.children[0].show(depth + 1)
    for i, x in enumerate(self.children[1]):
      ASTUtils.println('Argument {0}:'.format(str(i)), depth)
      x.show(depth + 1)

class ASTIdentifiers(ASTNode):
  def __init__(self, tree):
    if tree.value == 'Identifier':
      self.children = [tree.lexeme]
    else:
      self.children = ASTUtils.get_ids_list(tree)

  def show(self, depth = 0):
    ASTUtils.println('ASTIdentifiers: {0}'.format(str(self)), depth)

  def __str__(self):
    return '.'.join(self.children)

class ASTArrayCreation(ASTNode):
  # Children is of length 2:
  # 0. ASTType
  # 1. Expression corresponding to array length
  def __init__(self, tree):
    self.children = [ASTType(tree.children[1]),
                     ASTExpression.get_expr_node(tree.children[3])]
