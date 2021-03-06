import code_gen.asm.common as common
import code_gen.manager as manager

from ast_cast import ASTCast
from ast_node import ASTNode, ASTUtils
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

  def c_gen_code(self):
    import code_gen.access as access
    left_asm = self.left.c_gen_code()
    left_t = self.left.expr_type
    if left_t.is_array:
      return access.get_array_field(self.right, left_asm)
    return access.get_field_from_parts(left_t, self.right, left_asm)

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
      return self._handle_escapes(self.children[0])
    elif self.literal_type == ASTLiteral.INT:
      return int(self.children[0])
    elif self.literal_type == ASTLiteral.NULL:
      return None   # null is not considered a constant value (JLS 15.28)
    elif self.literal_type == ASTLiteral.STRING:
      return self._handle_escapes(self.children[0])

  def _handle_escapes(self, string):
    chars = list(string[1:-1])
    escaped_chars = []

    while len(chars) > 0:
      if chars[0] == '\\' and len(chars) > 1:
        # Check for octal digits.
        numeric = list('01234567')
        octal = []
        for i in range(0, min(3, len(chars) - 1)):
          if chars[1 + i] in numeric:
            octal.append(chars[1 + i])
          else:
            break

        if len(octal) > 0:
          if len(octal) == 3 and octal[0] in list('4567'):
            # Remove last digit.
            octal.pop()

          escaped_chars.append(chr(int(''.join(octal), 8)))
          for x in octal:
            chars.pop(0)
          # Remove the starting slash.
          chars.pop(0)
          continue

        new_chars = {
          '\\': '\\',
          '\'': '\'',
          '"': '"',
          'r': '\r',
          'f': '\f',
          'n': '\n',
          't': '\t',
          'b': '\b',
        }
        new_char = new_chars[chars[1]]
        escaped_chars.append(new_char)
        chars.pop(0)
        chars.pop(0)
      else:
        new_char = chars.pop(0)
        escaped_chars.append(new_char)

    return ''.join(escaped_chars)

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
    elif self.literal_type in [ASTLiteral.INT, ASTLiteral.CHAR]:
      value = self.const_value
      if self.literal_type == ASTLiteral.CHAR:
        if len(self.const_value) == 2:
          import pdb; pdb.set_trace()
        value = ord(self.const_value)

      return [
          'push {0}'.format(value),
          'call _create_int',
          'pop ebx ; pop to garbage',
          '; _create_int will store the address in eax'
      ]
    elif self.literal_type == ASTLiteral.NULL:
      return [
        'mov eax, 0',
      ]
    elif self.literal_type == ASTLiteral.STRING:
      # For a string literal we want to call the java.lang.String constructor
      # with an array of chars corresponding to the literal value.

      # XXX: Hack to get the array label.
      char_array_label = manager.CodeGenManager.primitive_array_create_labels['char']

      string_defn = self.expr_type.definition
      # XXX: Make this cleaner.
      constructor = string_defn.methods[3]

      string_value = self.const_value

      char_store_code = []
      for ix, char in enumerate(string_value):
        char_value = ord(char)
        char_offset = 12 + 4 * ix
        char_store_code.extend([
          'push {0}'.format(char_value),
          'call _create_int',
          'pop ebx ; pop to garbage',
          'mov [ecx + {0}], eax'.format(char_offset),
        ])

      return [
        '; storing the string literal {0}'.format(self.children[0]),
        'push {0} ; string length'.format(len(string_value)),
        'call _create_int',
        'pop ebx ; pop to garbage',
        'push eax',
        'call {0}'.format(char_array_label),
        'pop ebx ; pop to garbage',
        'mov ecx, eax ; ecx points to char array',
        '; start storing chars',
        char_store_code,
        '; done storing chars',
        '; allocate a string object',
        'call {0}'.format(string_defn.c_create_object_function_label),
        'push eax ; push instance',
        'push ecx ; push chars array',
        'call {0} ; call constructor'.format(constructor.c_defn_label),
        'pop ecx ; pop chars array',
        'pop eax ; restore instance to eax',
      ]

    raise Exception('Unhandled literal code gen case.')


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

  def c_gen_code(self):
    op_map = {
        '!': '_negate_bool',
        '-': '_negate_int',
    }

    return [
      common.store_param(self.expr),
      'call {0}'.format(op_map[self.operator]),
      'pop ebx ; pop to garbage',
      '; eax contains a pointer to the result',
    ]

class ASTAssignment(ASTExpression):
  def __init__(self, tree):
    # Two children:
    #   0. The expression on the left side of the assignment. It should be one
    #      of ASTIdentifiers, ASTFieldAccess or ASTArrayAccess.
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

  def c_gen_code(self):
    import code_gen.access as access
    result = self.right.c_gen_code()

    # The left hand side is either an ASTArrayAccess, ASTFieldAccess or
    # ASTIdentifiers.
    if isinstance(self.left, ASTIdentifiers):
      # For assignment expressions, we evaluate the left hand side first. If
      # the left hand side is an ASTIdentifiers, the same ASTIdentifiers could
      # be used on the right hand side in an assignment.
      # Thus, we must store a reference to where the left hand side points
      # before evaluating the right hand side.

      if self.left.is_simple:
        # If the left hand side is simple, it is either a method parameter,
        # local variable or an instance field on the enclosing type. The
        # location for all of these cannot be altered by the right hand side,
        # so we can calculate the right hand side first.
        return [
          result,
          access.set_simple_var(self.left.simple_decl, 'eax'),
        ]
      else:
        import code_gen.annotate_ids as annotate_ids

        annotations = annotate_ids.annotate_identifier(self.left)
        if len(annotations) == 0:
          # If we do not have any annotations then the left hand side is a
          # static field. This address cannot change.
          return [
            result,
            access.set_simple_static_field(self.left, 'eax'),
          ]
        else:
          # _get_to_final provides code to store a pointer to the second last
          # part of the identifier in $eax.
          type_, code = access._get_to_final(self.left, annotations)
          env = type_.definition.environment

          final_part = str(self.left.parts[-1])
          f, _ = env.lookup_field(final_part)

          return [
            code,
            common.check_null('eax'),
            'push eax ; save instance that we want to store a field on',
            result,
            'pop ebx ; instance to store a field on',
            common.save_instance_field('ebx', f, 'eax'),
          ]

    elif isinstance(self.left, ASTFieldAccess):
      left_asm = self.left.left.c_gen_code()
      left_t = self.left.left.expr_type
      if left_t.is_array:
        raise Exception('Trying to write to array field')
      return [
        '; FieldAccess assignment',
        access.get_field_from_parts(
            left_t, self.left.right, left_asm, get_addr=True),
        'push eax  ; Save field addr',
        result,
        '; RHS of assignment should be eax',
        'pop ebx  ; Pop addr of field',
        'mov [ebx], eax  ; Assign!'
      ]

    elif isinstance(self.left, ASTArrayAccess):
      array_soundness_pass = manager.CodeGenManager.get_label('array_soundness_pass')

      soundness_asm = []
      if not self.left.array_expression.expr_type.is_primitive:
        soundness_asm = [
          'push eax',
          'push ebx',
          'push ecx',
          '; Get CIT of right side',
          'mov ecx, [ecx]'
          '; Get subtype col of right side',
          'mov ecx, [ecx + 4]',
          '; get subtype offset',
          'mov ebx, [ebx + 4]',
          '; index into subtype col',
          'mov ecx, [ecx + ebx]',
          'cmp ecx, 1  ; 1 means that RHS is a subtype of LHS',
          'je {0}'.format(array_soundness_pass),
          'call __exception',
          '{0}:'.format(array_soundness_pass),
          'pop ecx',
          'pop ebx',
          'pop eax',
        ]

      # The result is calculated after the array index offset.
      return [
        self.left.c_gen_code_get_array_pointer(),
        'push ebx ; save array pointer',
        'push eax ; save array offset',
        result,
        'mov ecx, eax ; move result',
        'pop eax ; restore array offset',
        'pop ebx ; restore array pointer',
        '; do array type soundness check',
        soundness_asm,
        'mov [ebx + eax], ecx',
        'mov eax, ecx ; result should be in eax',
      ]

    raise Exception('Programmer error: trying to assign to invalid AST')


class ASTArrayAccess(ASTExpression):
  def __init__(self, tree):
    # Two children:
    #   0. The expression that will (should) return an array.
    #   1. An expression that determines the index into the array.
    self.children = [ASTExpression.get_expr_node(tree.children[0]),
                     ASTExpression.get_expr_node(tree.children[2])]
    super(ASTArrayAccess, self).__init__()


  def c_gen_code_get_array_pointer(self):
    '''Creates code that will store the array a reference to the array in ebx
    and the offset for the index in eax.'''
    array_check_pass = manager.CodeGenManager.get_label('array_check_pass')
    array_check_fail = manager.CodeGenManager.get_label('array_check_fail')

    # Assume that we're doing an array read.
    return [
      self.array_expression.c_gen_code(),
      common.check_null('eax'),
      'push eax',
      self.index.c_gen_code(),
      'pop ebx   ; restore the pointer to the array',
      common.unwrap_primitive('eax', 'eax'),
      '; check whether the index is out of bounds:',
      common.get_array_length('ecx', 'ebx'),
      common.unwrap_primitive('ecx', 'ecx'),
      'cmp eax, ecx',
      'jge {0}'.format(array_check_fail),
      'cmp eax, 0',
      'jl {0}'.format(array_check_fail),
      'jmp {0}'.format(array_check_pass),
      '{0}:'.format(array_check_fail),
      'call __exception',

      '{0}:'.format(array_check_pass),
      '; calculate the offset into the array:',
      'imul eax, 4',
      'add eax, 12',
    ]

  def c_gen_code(self):
    return [
      self.c_gen_code_get_array_pointer(),
      'mov eax, [ebx + eax]',
    ]

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

  def c_gen_code(self):
    return [
      common.get_param('eax', 0, manager.CodeGenManager.N_PARAMS)
    ]

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
  def arg_types(self):
    return [x.expr_type for x in self.children[1]]

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

  def c_gen_code(self):
    '''Generate method invocation code'''
    import code_gen.invoke as invoke
    import code_gen.annotate_ids as annotate_ids

    # Get the ASM to push the arguments on the stack left to right.
    args_asm = invoke.get_arg_list(self.arguments)

    # Simple case: The method invocation is just off an ASTIdentifiers.
    if self.right is None:
      ids = self.left
      if len(ids.parts) == 1:
        # Method invocation off implcit "this".  Joos does not allow static
        # methods to be called with an implcit type.
        code = [
          '; Put "this" in eax before calling implicit this method',
          common.get_param('eax', 0, manager.CodeGenManager.N_PARAMS)
        ]
        this_type = manager.CodeGenManager.cur_method.parent_type
        return invoke.call_method_with_final(
            this_type, ids, code, self.arg_types, args_asm)

      annotation = annotate_ids.annotate_identifier(ids)
      if len(annotation) == 0:
        # Call a static method m, since we have handled the implcit "this"
        # case above.
        return invoke.call_static_method(ids, self.arg_types, args_asm)
      return invoke.call_simple_method(ids, self.arg_types, args_asm)

    # If we have a right side, then the left side should be evaluated and
    # the method should be taken off that side.
    left_asm = self.left.c_gen_code()
    left_t = self.left.expr_type
    return invoke.call_method_parts(
        left_t, self.right, left_asm, self.arg_types, args_asm)

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
  def left(self):
    return self.children[0]

  @property
  def expressions(self):
    '''Returns a list of all ASTExpression children.'''
    return [self.children[0]]

  def c_gen_code(self):
    subtype_offset = 4 * manager.CodeGenManager.get_subtype_table_index(
        self.type_node)
    not_null_label = manager.CodeGenManager.get_label('instanceof_not_null')
    done_label = manager.CodeGenManager.get_label('instanceof_done')
    return [
      self.left.c_gen_code(),
      # Null check.
      'mov ebx, 0',
      'cmp eax, ebx',
      'jne {0}'.format(not_null_label),
      'push 0',
      'jmp {0}'.format(done_label),
      '{0}:'.format(not_null_label),
      common.unwrap_subtype_col_from_object('eax', 'eax'),
      'mov eax, [eax + {0}]'.format(subtype_offset),
      'push eax',
      '{0}:'.format(done_label),
      'call _create_boolean',
      'pop ebx ; pop param',
    ]

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
    # Quickly handle string concat to avoid multiple code gens of children.
    if self.operator == '+' and str(self.expr_type) == 'java.lang.String':
      import code_gen.string
      return code_gen.string.string_concat(self)

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
        '>': '_greater_than',
        '>=': '_greater_than_eq',
        '<': '_less_than',
        '<=': '_less_than_eq',
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
    elif self.operator == '==' or self.operator == '!=':
      # For == and !=, we have to handle primitive types and references types
      # differently.
      equality_ops = {
        '==': ['_equals_prim', '_equals_ref'],
        '!=': ['_not_equals_prim', '_not_equals_ref'],
      }
      if self.left_expr.expr_type.is_primitive:
        op_function = equality_ops[self.operator][0]
      else:
        op_function = equality_ops[self.operator][1]

      return [
          left_operand,
          right_operand,
          'call {0}'.format(op_function),
          'pop ebx  ; pop second param',
          'pop ebx  ; pop first param',
          '; eax contains a pointer to the result'
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
      'call {0}'.format(class_defn.c_create_object_function_label),
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

  @property
  def is_simple(self):
    '''Returns whether this set of identifiers is a simple name.'''
    return self.first_definition[0] == str(self)

  @property
  def simple_decl(self):
    return self.first_definition[1]

  def c_gen_code(self):
    import code_gen.annotate_ids as annotate_ids
    import code_gen.access as access
    # Handle the case of a simple name.
    if self.is_simple:
      return access.get_simple_var(self.simple_decl)

    annotation = annotate_ids.annotate_identifier(self)
    if len(annotation) == 0:
      # We should only reach this point if we're trying to resolve
      # ClassName.f, ie. a static field access directly off the type.
      return access.get_simple_static_field(self)

    return access.get_field_access_from_annotation(self, annotation)

class ASTArrayCreation(ASTExpression):
  # Children is of length 2:
  # 0. ASTType
  # 1. Expression corresponding to array length
  def __init__(self, tree):
    self.children = [ASTType(tree.children[1]),
                     ASTExpression.get_expr_node(tree.children[3])]
    super(ASTArrayCreation, self).__init__()

  def c_gen_code(self):
    class_defn = self.type_node.definition
    array_create_fn_label = ''
    if class_defn is None:
      # This is a primitive type.
      prim_name = self.type_node.children[0]
      array_create_fn_label = \
          manager.CodeGenManager.primitive_array_create_labels[prim_name]
    else:
      array_create_fn_label = class_defn.c_create_array_function_label

    return [
      self.children[1].c_gen_code(),
      'push eax  ; array length',
      'call {0}'.format(array_create_fn_label),
      'pop ebx  ; pop to garbage',
    ]

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
