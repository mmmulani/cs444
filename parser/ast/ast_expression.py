import code_gen.asm.common as common
import code_gen.manager as manager

from ast_node import ASTNode, ASTUtils
from ast_cast import ASTCast
from ast_type import ASTType
from ast_variable_declaration import ASTVariableDeclaration

class ASTExpression(ASTNode):
  '''General ASTExpression class with a function to create the proper ASTNode'''

  def __init__(self):
    self.expr_type = None
    self.const_value = None

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
      possible_binary_rules = [
          'ConditionalOrExpression', 'ConditionalAndExpression',
          'InclusiveOrExpression', 'ExclusiveOrExpression', 'AndExpression',
          'EqualityExpression', 'RelationalExpression', 'AdditiveExpression',
          'MultiplicativeExpression']

      # If it's not one of the possible binary types, we're in trouble...
      if child.value not in possible_binary_rules:
        raise ASTExpressionError(
            'Invalid binary expression type "{0}"'.format(child.value))

      return make_ast_binary_node(child)

    raise ASTExpressionError('Unhandled Expression')

def make_ast_binary_node(tree):
  op = tree.children[1].lexeme
  if op == 'instanceof':
    return ASTInstanceOf(tree)
  return ASTBinary(tree)

class ASTExpressionError(Exception):
  pass

class ASTFieldAccess(ASTExpression):
  def __init__(self, tree):
    self.children = [
        ASTExpression.get_expr_node(tree.children[0]),
        ASTIdentifiers(tree.children[2])]
    super(ASTFieldAccess, self).__init__()

  @property
  def left(self):
    return self.children[0]

  @property
  def right(self):
    return self.children[1]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return list(self.children)

  def show(self, depth = 0, types = False):
    ASTUtils.println(
      'ASTFieldAccess {0}'.format(ASTUtils.type_string(self.expr_type, types)),
      depth)
    self.children[0].show(depth + 1, types)
    self.children[1].show(depth + 1, False)

class ASTLiteral(ASTExpression):
  # Enum of different literal types.
  BOOLEAN = 'boolean'
  CHAR = 'char'
  INT = 'int'
  NULL = 'null'
  STRING = 'string'

  def __init__(self, tree):
    super(ASTLiteral, self).__init__()
    self.children = [tree.lexeme]
    self.literal_type = self._get_literal_type(tree.lexeme)

    self.const_value = self._get_literal_value()

  def show(self, depth = 0, types = False):
    ASTUtils.println(
        'Literal of type {0}: {1} {2}'.format(self.literal_type,
        self.children[0], ASTUtils.type_string(self.expr_type, types)), depth)

  def _get_literal_type(self, literal):
    # At this stage, we have already weeded out literals not of one of the types
    # in the enum.
    if literal in ['true', 'false']:
      return ASTLiteral.BOOLEAN
    elif literal[0] == '\'':
      return ASTLiteral.CHAR
    elif literal.isdigit():
      return ASTLiteral.INT
    elif literal == 'null':
      return ASTLiteral.NULL
    elif literal[0] == '"':
      return ASTLiteral.STRING

    raise Exception('Bad literal: {0}'.format(literal))

  def _get_literal_value(self):
    '''Convert the string of the literal into its real value (int, bool, etc)'''
    if self.literal_type == ASTLiteral.BOOLEAN:
      return self.children[0] == 'true'
    elif self.literal_type == ASTLiteral.CHAR:
      return self.children[0].strip('\'')
    elif self.literal_type == ASTLiteral.INT:
      return int(self.children[0])
    elif self.literal_type == ASTLiteral.NULL:
      return None   # null is not considered a constant value (JLS 15.28)
    elif self.literal_type == ASTLiteral.STRING:
      return self.children[0].strip('"')

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return []

  # Code gen functions start here.

  def c_gen_code(self):
    if self.literal_type == ASTLiteral.BOOLEAN:
      if self.const_value:
        boolean_as_int = 1
      else:
        boolean_as_int = 0

      return [
          'push {0}'.format(boolean_as_int),
          'call _create_boolean',
          'pop ebx ; pop to garbage',
          '; _create_boolean will store the address in eax',
      ]
    elif self.literal_type == ASTLiteral.INT:
      return [
          'push {0}'.format(self.const_value),
          'call _create_int',
          'pop ebx ; pop to garbage',
          '; _create_int will store the address in eax'
      ]
    elif self.literal_type == ASTLiteral.NULL:
      return [
        '; no params',
        'call _create_null',
        '; _create_null stores the address in eax'
      ]
    else:
      return []


class ASTUnary(ASTExpression):
  def __init__(self, tree):
    # TODO: Convert operator to an enum?
    # One child, the single unary expression after the operator.
    self.operator = tree.children[0].lexeme
    self.children = [ASTExpression.get_expr_node(tree.children[1])]
    super(ASTUnary, self).__init__()

  def show(self, depth = 0, types = False):
    ASTUtils.println(
      'ASTUnary, operator: {0} {1}'.format(self.operator,
          ASTUtils.type_string(self.expr_type)), depth)
    ASTUtils.println('Operand:', depth)
    self.children[0].show(depth + 1, types)

  @property
  def expr(self):
    return self.children[0]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    # Copy this array so the caller can modify it.
    return [self.children[0]]

class ASTAssignment(ASTExpression):
  def __init__(self, tree):
    # Two children:
    #   0. The expression on the left side of the assignment.
    #   1. The expression on the right side of the assignment.
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]
    super(ASTAssignment, self).__init__()

  @property
  def left(self):
    return self.children[0]

  @property
  def right(self):
    return self.children[1]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    # Copy this array so the caller can modify it.
    return [self.children[0], self.children[1]]

  @property
  def left_expr(self):
    return self.children[0]

  @property
  def right_expr(self):
    return self.children[1]

class ASTArrayAccess(ASTExpression):
  def __init__(self, tree):
    # Two children:
    #   0. The expression that will (should) return an array.
    #   1. An expression that determines the index into the array.
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]
    super(ASTArrayAccess, self).__init__()

  @property
  def array_expression(self):
    return self.children[0]

  @property
  def index(self):
    return self.children[1]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    # Copy this array so the caller can modify it.
    return list(self.children)

class ASTThis(ASTExpression):
  def __init__(self, tree):
    self.children = []
    super(ASTThis, self).__init__()

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return []

  def show(self, depth = 0, types = False):
    ASTUtils.println('ASTThis {0}'.format(ASTUtils.type_string(
        self.expr_type)), depth)

class ASTMethodInvocation(ASTExpression):
  def __init__(self, tree):
    self.children = [[], []]
    # self.children is of length 2:
    # 0. List of length 1 or 2.
    #    If length 1, it is just an ASTIdentifiers.
    #    If length 2, the first is an arbitrary expression and the second is an
    #    identifier (a field access of the first).
    #    e.g.:
    #      (i.j).k => [Expression for "(i.j)", Expression for "k"]
    # 1. List of argument expressions (possibly empty)
    if tree.children[0].value == 'Identifiers':
      self.children[0] = [ASTExpression.get_expr_node(tree.children[0])]
      if tree.children[2].value == 'ArgumentList':
        self.children[1] = ASTUtils.get_arg_list(tree.children[2])
    else:
      prefix_exprs = [ASTExpression.get_expr_node(tree.children[0]),
                      ASTExpression.get_expr_node(tree.children[2])]

      arg_list = []
      if tree.children[4].value == 'ArgumentList':
        arg_list = ASTUtils.get_arg_list(tree.children[4])

      self.children = [prefix_exprs, arg_list]


    # The ASTMethod for the method invocation.  This will be set during type
    # checking.
    self.method_definition = None
    super(ASTMethodInvocation, self).__init__()

  def show(self, depth = 0, types = False):
    ASTUtils.println('ASTMethodInvocation {0}'.format(
        ASTUtils.type_string(self.expr_type, types)), depth)
    if len(self.children[0]) == 1:
      ASTUtils.println('Method identifiers:', depth)
      self.children[0][0].show(depth + 1, types=False)
    else:
      ASTUtils.println('Expression:', depth)
      self.children[0][0].show(depth + 1, types)
      ASTUtils.println('Field access from expression:', depth)
      self.children[0][1].show(depth + 1, types=False)
    for i, x in enumerate(self.children[1]):
      ASTUtils.println('Argument {0}:'.format(str(i)), depth)
      x.show(depth + 1, types)

  @property
  def arguments(self):
    return self.children[1]

  @property
  def left(self):
    return self.children[0][0]

  @property
  def right(self):
    if len(self.children[0]) == 2:
      return self.children[0][1]
    else:
      return None

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return self.children[0] + self.children[1]

class ASTInstanceOf(ASTExpression):
  def __init__(self, tree):
    # x instanceof y
    # Two children.
    #   0. ASTExpression, x
    #   1. ASTType for y
    self.children = [
        ASTExpression.get_expr_node(tree.children[0]),
        ASTType(tree.children[2])]

    self.type_node = self.children[1]

    super(ASTInstanceOf, self).__init__()

  def show(self, depth = 0, types = False):
    ASTUtils.println(
        'ASTInstanceOf Type: {0} {1}'.format(str(self.type_node),
            ASTUtils.type_string(self.expr_type)), depth)
    self.children[0].show(depth + 1, types)

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return [self.children[0]]

class ASTBinary(ASTExpression):
  def __init__(self, tree):
    # TODO: convert operator to enum?
    # Children is [left operand, right operand].
    self.operator = tree.children[1].lexeme
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]
    super(ASTBinary, self).__init__()

  def show(self, depth = 0, types = False):
    ASTUtils.println('ASTBinary, operator: {0} {1}'.format(self.operator,
        ASTUtils.type_string(self.expr_type, types)), depth)
    ASTUtils.println('Left operand:', depth)
    self.children[0].show(depth + 1, types)
    ASTUtils.println('Right operand:', depth)
    self.children[1].show(depth + 1, types)

  @property
  def left_expr(self):
    return self.children[0]

  @property
  def right_expr(self):
    return self.children[1]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return [self.children[0], self.children[1]]

  def c_gen_code(self):
    # We provide the code to generate the value of each operand separately as
    # some operators (e.g. &&) will not necessarily evaluate both.
    left_operand = common.store_param(self.left_expr)
    right_operand = common.store_param(self.right_expr)

    lazy_ops = {
        '+': '_add_int',
        '-': '_sub_int',
        '*': '_mult_int',
        '/': '_divide_int',
        '%': '_mod_int',
        '&': '_eager_and',
        '|': '_eager_or',
    }

    if self.operator in lazy_ops.keys():
      op_function = lazy_ops[self.operator]
      return [
          left_operand,
          right_operand,
          'call {0}'.format(op_function),
          'pop ebx  ; pop second param',
          'pop ebx  ; pop first param',
          '; eax contains a pointer to the result'
      ]
    elif self.operator == '&&':
      done_eval = manager.CodeGenManager.get_label('done_and_and_operator')
      return [
          '; start &&',
          common.if_false(self.left_expr, done_eval),
          self.right_expr.c_gen_code(),
          '{0}:'.format(done_eval),
          '; eax contains a pointer to the result',
          '; end &&',
      ]
    elif self.operator == '||':
      done_eval = manager.CodeGenManager.get_label('done_or_or_operator')
      return [
          '; start ||',
          common.if_true(self.left_expr, done_eval),
          self.right_expr.c_gen_code(),
          '{0}:'.format(done_eval),
          '; eax contains a pointer to the result',
          '; end ||',
      ]

    return []

class ASTClassInstanceCreation(ASTExpression):
  def __init__(self, tree):
    # Children is of length 2:
    # 0. ASTType corresponding to class type.
    # 1. List of arguments (possibly empty).
    self.children = [ASTType(tree.children[1].children[0]), []]

    if tree.children[3].value == 'ArgumentList':
      self.children[1] = ASTUtils.get_arg_list(tree.children[3])

    super(ASTClassInstanceCreation, self).__init__()

  def show(self, depth = 0, types = False):
    ASTUtils.println('ASTClassInstanceCreation {0}'.format(
        ASTUtils.type_string(self.expr_type)), depth)
    ASTUtils.println('Class type:', depth)
    self.children[0].show(depth + 1, types)
    for i, x in enumerate(self.children[1]):
      ASTUtils.println('Argument {0}:'.format(str(i)), depth)
      x.show(depth + 1, types)

  @property
  def type_node(self):
    return self.children[0]

  @property
  def arguments(self):
    return self.children[1]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return self.children[1]

  def c_gen_code(self):
    class_defn = self.type_node.definition
    param_code = [common.store_param(x) for x in self.arguments]
    pop_params = ['pop ebx ; pop param to garbage' for x in self.arguments]
    sig = (str(class_defn.name), [x.expr_type for x in self.arguments])
    constructor, _ = class_defn.environment.lookup_method(sig, constructor=True)

    if constructor is None:
      raise Exception(
          'Could not match instance creation expression with constructor')

    return [
      common.malloc(class_defn.c_object_size),
      # Class info table
      'mov dword [eax], {0}'.format(class_defn.c_class_info_table_label),
      'push eax ; push instance object',
      param_code,
      'call {0}'.format(constructor.c_defn_label),
      pop_params,
      'pop eax ; restore the instance to eax',
    ]

class ASTIdentifiers(ASTExpression):
  def __init__(self, tree):
    if isinstance(tree, str):
      # Allow creating an ASTIdentifiers node directly from a string.
      self.children = tree.split('.')
    elif tree.value == 'Identifier':
      self.children = [tree.lexeme]
    else:
      self.children = ASTUtils.get_ids_list(tree)

    self.first_definition = (None, None)
    super(ASTIdentifiers, self).__init__()

  def show(self, depth = 0, types = False):
    ASTUtils.println('ASTIdentifiers: {0} {1}'.format(str(self),
        ASTUtils.type_string(self.expr_type, types)), depth)

  def __str__(self):
    return '.'.join(self.children)

  def __eq__(a, b):
    return a.children == b.children

  @property
  def parts(self):
    return list(self.children)

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return []

  def c_gen_code(self):
    # XXX: Hack to test local variables.
    '''
    defn = self.first_definition[1]
    if isinstance(defn, ASTVariableDeclaration):
      return common.get_local_var('eax', defn)
    else:
      return ''
    '''
    return ''

class ASTArrayCreation(ASTExpression):
  # Children is of length 2:
  # 0. ASTType
  # 1. Expression corresponding to array length
  def __init__(self, tree):
    self.children = [ASTType(tree.children[1]),
                     ASTExpression.get_expr_node(tree.children[3])]
    super(ASTArrayCreation, self).__init__()

  @property
  def type_node(self):
    return self.children[0]

  @property
  def length_expr(self):
    return self.children[1]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return [self.children[1]]
