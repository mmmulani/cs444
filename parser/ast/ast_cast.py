import ast_expression
import ast_node
import ast_type
import code_gen.asm.common as common

from code_gen.manager import CodeGenManager

class ASTCast(ast_node.ASTNode):
  def __init__(self, tree):
    '''Creates an AST Cast node from a 'CastExpression' TreeNode'''

    # Two children.
    #   0. A type node going to the type, and
    #   1. An expression node for the expression

    self.children = [self._create_type_node(tree),
        ast_expression.ASTExpression.get_expr_node(tree.children[-1])]
    self.expr_type = None
    self.const_value = None

  @property
  def type_node(self):
    return self.children[0]

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

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println(
        'ASTCast Type: {0} {1}'.format(self.children[0],
            ast_node.ASTUtils.type_string(self.expr_type)), depth)
    self.children[1].show(depth + 1, types)

  @property
  def expressions(self):
    return [self.children[1]]

  def c_gen_code(self):
    from ast_expression import ASTLiteral

    if self.type_node.is_primitive and not self.type_node.is_array:
      primitive_sizes = {
        'boolean': 0x1,
        'byte': 0xff,
        'char': 0xff,
        'int': 0xffffffff,
        'null': 0x0,
        'short': 0xffff,
      }

      expr_size = primitive_sizes[str(self.expressions[0].expr_type)]
      result_size = primitive_sizes[str(self.type_node)]

      # Widen all numeric types but chars.
      widen_code = []
      if str(self.expressions[0].expr_type) in ['byte', 'short']:
        done_label = CodeGenManager.get_label('cast_widen_done')
        if expr_size == 0xff:
          widen_code = [
            'mov ebx, eax',
            'and ebx, 0x80',
            'cmp ebx, 0x80',
            'jne {0}'.format(done_label),
            'or eax, 0xffffff00',
            '{0}:'.format(done_label),
          ]
        elif expr_size == 0xffff:
          widen_code = [
            'mov ebx, eax',
            'and ebx, 0x8000',
            'cmp ebx, 0x8000',
            'jne {0}'.format(done_label),
            'or eax, 0xffff0000',
            '{0}:'.format(done_label),
          ]

      return [
        self.expressions[0].c_gen_code(),
        common.unwrap_primitive('eax', 'eax'),
        widen_code,
        'and eax, {0} ; narrow to {1}'.format(result_size, str(self.type_node)),
        'push eax ; create new primitive with value',
        'call _create_int',
        'pop ebx ; pop param',
      ]
    else:
      subtype_offset = 4 * CodeGenManager.get_subtype_table_index(
          self.type_node)

      finished_label = CodeGenManager.get_label('cast_exp_finished')
      return [
        self.expressions[0].c_gen_code(),
        # Null check.
        'mov ebx, 0',
        'cmp eax, ebx',
        'je {0}'.format(finished_label),
        common.unwrap_subtype_col_from_object('ebx', 'eax'),
        'mov ebx, [ebx + {0}]'.format(subtype_offset),
        'mov ecx, 1',
        'cmp ebx, ecx',
        'je {0}'.format(finished_label),
        '; OH NO! CastException!',
        'call __exception',
        '{0}:'.format(finished_label),
      ]


class ASTCastError(Exception):
  pass
