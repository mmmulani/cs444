import ast_expression
import ast_method
import ast_node
import ast_type
import ast_variable_declaration
import code_gen.cit.cit as cit

from code_gen.manager import CodeGenManager

class ASTClass(ast_node.ASTNode):
  def __init__(self, tree, package_name=''):
    '''Create an AST Class Declaration node'''
    # Two children.
    #   0. List of fields.
    #   1. List of methods.
    self.fields = []
    self.methods = []
    self.children = self._get_children(tree)

    self._modifiers = self._get_modifiers(tree)
    self.name = self._get_name(tree)
    self.super = self._get_super_class(tree)
    self.interfaces = self._get_interfaces(tree)

    self.canonical_name = str(self.name)
    self.package_name = package_name
    if package_name != '':
      self.canonical_name = '{0}.{1}'.format(package_name, self.name)

    # If the class doesn't extend anything, then it should extend
    # java.lang.Object by default unless it is java.lang.Object itself.
    if len(self.super) == 0 and self.canonical_name != 'java.lang.Object':
      self.super = [ast_type.ASTType.from_str('java.lang.Object')]

    # This is set by the Environment module when the tree is complete.
    self.environment = None

    # The size of the object.  This is 4 + (# of instance fields), with 4 bytes
    # needed for the pointer to the CIT.  This will be modified during the
    # code generation stage.
    self.c_object_size = 4

    # The current maximum offset for any method or field of this type.  This
    # starts at 8 because the CIT is layed out as:
    #
    # --------
    # Pointer to SIT
    # --------
    # Pointer to subtype table
    # --------
    # Methods and Static Fields
    # . . .
    self.c_max_offset = 8

    # Whether offset calculation has finished on this type.
    self.c_has_offset = False

    # Set by the Selector Index Table script in the code gen stage.
    self.c_sit_column = []
    # Set by the c_sit_column_label property. It is an assembly label for the
    # SIT column.
    self._c_sit_column_label = None

    # Set by the Subtype Table script in the code gen stage.
    self.c_subtype_column = None

  def show(self, depth = 0, types = False):
    ast_node.ASTUtils.println('Class: {0}'.format(self.name), depth)

    if len(self.modifiers) > 0:
      ast_node.ASTUtils.println('Modifiers: {0}'.format(
          ', '.join(self.modifiers)), depth)

    if self.super:
      ast_node.ASTUtils.println(
          'Extends: {0}'.format('.'.join(self.super[0].children[0].children)),
          depth)

    if len(self.interfaces) > 0:
      ifaces = []
      for ast_ids in self.interfaces:
        ifaces.append('.'.join(ast_ids.children[0].children))
      ast_node.ASTUtils.println(
          'Implements: {0}'.format(', '.join(ifaces)), depth)

    if len(self.fields) > 0:
      ast_node.ASTUtils.println('Fields:', depth)
      for f in self.fields:
        f.show(depth + 1, types)

    if len(self.methods) > 0:
      for m in self.methods:
        ast_node.ASTUtils.println('Method:', depth)
        m.show(depth + 1, types)

  @property
  def modifiers(self):
    return list(self._modifiers)

  @property
  def is_final(self):
    return ('final' in self._modifiers)

  @property
  def is_abstract(self):
    return ('abstract' in self._modifiers)

  @property
  def has_super(self):
    return len(self.super) > 0

  def get_all_methods(self):
    '''Returns all the methods in the contains set of this class'''
    return self.environment.get_all_methods()

  def get_all_fields(self):
    '''Returns all fields in the contains set of this type'''
    return self.environment.get_all_fields()

  def _get_children(self, tree):
    '''Get a list of fields from a class declaration'''
    node = tree.children[-1]
    if node.value != 'ClassBody':
      raise ASTClassError('Class body is not the last child of class decl.')
    if len(node.children) <= 2:
      # No declarations.
      return [[], []]

    # Process each declaration.
    node = node.children[1]
    while len(node.children) > 1:
      decl = node.children[1]  # ClassBodyDeclaration
      self._handle_decl(decl.children[0])
      node = node.children[0]
    self._handle_decl(node.children[0].children[0])

    # Reverse the lists to put them in declaration order.
    self.fields.reverse()
    self.methods.reverse()
    return [self.fields, self.methods]

  def _handle_decl(self, tree):
    '''Handle a single class declaration'''
    decl = tree
    if decl.value == 'ConstructorDeclaration':
      self.methods.append(ast_method.ASTMethod(decl))
      return

    # Field/member declarations are one level deeper
    if decl.children[0].value == 'FieldDeclaration':
      self.fields.append(ast_variable_declaration.ASTVariableDeclaration(
          decl.children[0]))
    elif decl.children[0].value == 'MethodDeclaration':
      self.methods.append(ast_method.ASTMethod(decl.children[0]))
    elif decl.children[0].value == ';':
      pass

  def _get_modifiers(self, tree):
    '''Get a set of modifiers for a class declaration'''
    if tree.children[0].value != 'Modifiers':
      return set()
    return ast_node.ASTUtils.get_modifiers_set(tree.children[0])

  def _get_name(self, tree):
    '''Get the name of a class from its declaration'''
    # Name child could be either second or third child depending on whether
    # the class has any modifiers.
    node = None
    if tree.children[1].value == 'Identifier':
      node = tree.children[1]
    elif tree.children[2].value == 'Identifier':
      node = tree.children[2]
    else:
      raise ASTClassError('Class has no name.')

    return ast_expression.ASTIdentifiers(node)

  def _get_super_class(self, tree):
    '''Get the superclass of a class from its declaration'''
    # Super_OPT can be either the third or fourth child depending on whether
    # the class has and modifiers.
    node = None
    if tree.children[2].value == 'Super':
      node = tree.children[2]
    elif tree.children[3].value == 'Super':
      node = tree.children[3]
    else:
      # Super is optional.
      return []

    # return a list, to match properties of ASTInterface
    return [ast_type.ASTType(node.children[1].children[0])]

  def _get_interfaces(self, tree):
    '''Get the interfaces the class implements from its declarations'''
    node = None
    if tree.children[3].value == 'Interfaces':
      node = tree.children[3]
    elif len(tree.children) > 4 and tree.children[4].value == 'Interfaces':
      node = tree.children[4]
    elif len(tree.children) > 5 and tree.children[5].value == 'Interfaces':
      node = tree.children[5]
    else:
      return []

    # Interfaces implements InterfaceTypeList
    # InterfaceTypeList InterfaceType
    # InterfaceTypeList InterfaceTypeList , InterfaceType
    # InterfaceType Identifiers
    node = node.children[1]
    ret = []
    while len(node.children) == 3:
      ret.append(ast_type.ASTType(node.children[2].children[0]))
      node = node.children[0]
    ret.append(ast_type.ASTType(node.children[0].children[0]))
    ret.reverse()
    return ret

  # ------ CODE GEN METHODS --------

  @property
  def c_sit_column_label(self):
    label = 'sit_column_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_subtype_column_label(self):
    label = 'subtype_column_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_class_info_table_label(self):
    label = 'class_info_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  def c_gen_code(self):
    '''Code generation for types'''
    # Generate code for all the methods.
    methods = []
    for m in self.methods:
      methods.extend([m.c_gen_code(), ''])

    return [
      methods,
      '', '',  # Padding before the SIT/Subtype columns.
      self.c_gen_code_sit_column(),
      '', '',  # Padding between tables.
      self.c_gen_code_subtype_column(),
      '', '',
      cit.generate_cit(self),
    ]

  def c_gen_code_sit_column(self):
    '''Generates assembly for the SIT table for this type.'''
    table_entries = []
    for ix, m in enumerate(self.c_sit_column):
      # Add an assembly comment to explain the row.
      selector = CodeGenManager.get_selector(ix)
      ret_type, (name, params) = selector
      param_strs = [str(t) for t in params]
      method_str = '{0} {1}({2})'.format(str(ret_type), name,
          ', '.join(param_strs))
      table_entries.append('; {0}'.format(method_str))

      entry = ''
      if m is None:
        entry = 'dd 0x0'
      else:
        entry = 'dd {0}'.format(m.c_defn_label)

      table_entries.append(entry)

    return [
        '{0}:'.format(self.c_sit_column_label),
        table_entries
    ]

  def c_gen_code_subtype_column(self):
    '''Generates assembly for the subtype table for this type'''
    # We use a helper as subtype columns for classes and interfaces are created
    # the same way.
    return ASTClass.c_gen_code_subtype_column_helper(
        self.c_subtype_column_label, self.c_subtype_column)

  @staticmethod
  def c_gen_code_subtype_column_helper(label, subtype_column):
    '''Generates the subtype column given the label and the values for the type

    subtype_column is a list of boolean values corresponding to whether the
    type is a subtype of the row type.'''
    subtype_cells = []
    for ix, val in enumerate(subtype_column):
      # Add a comment for each subtype cell.
      type_ = CodeGenManager.get_subtype_table_type(ix)
      subtype_cells.append('; subtype = {0}'.format(str(type_)))

      if val:
        subtype_cells.append('dd 1')
      else:
        subtype_cells.append('dd 0')

    return [
      '; EXAMPLE',
      '; subtype = X',
      '; dd 1',
      '; X is a subtype of the contained type',
      '{0}:'.format(label),
      subtype_cells
    ]

class ASTClassError(Exception):
  pass
