import ast_expression
import ast_method
import ast_node
import ast_type
import ast_variable_declaration
import code_gen.asm.array as array
import code_gen.asm.common as common
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

    # The current maximum offset for any instance field in the object.  This
    # starts at 4 because the first dword of an object is a pointer to the
    # CIT.
    self.c_obj_offset = 4
    self.c_has_obj_offset = False

    # The current maximum offset for any method or static field of this type in
    # its CIT. This starts at 8 because the CIT is layed out as:
    #
    # --------
    # Pointer to SIT
    # --------
    # Pointer to subtype table
    # --------
    # Methods and Static Fields
    # . . .
    self.c_cit_offset = 8

    # Whether offset calculation has finished on this type.
    self.c_has_cit_offset = False

    # Set by the Selector Index Table script in the code gen stage.
    self.c_sit_column = []
    # Set by the c_sit_column_label property. It is an assembly label for the
    # SIT column.
    self._c_sit_column_label = None

    # Set by the Subtype Table script in the code gen stage.
    self.c_subtype_column = None
    self.c_array_subtype_column = None

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
      self.methods.append(ast_method.ASTMethod(decl, self))
      return

    # Field/member declarations are one level deeper
    if decl.children[0].value == 'FieldDeclaration':
      self.fields.append(ast_variable_declaration.ASTVariableDeclaration(
          decl.children[0]))
    elif decl.children[0].value == 'MethodDeclaration':
      self.methods.append(ast_method.ASTMethod(decl.children[0], self))
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
  def c_array_sit_column_label(self):
    label = 'sit_column_{0}'.format(
        CodeGenManager.java_lang_object_defn.canonical_name)
    return CodeGenManager.memoize_label(CodeGenManager.java_lang_object_defn,
        label)

  @property
  def c_subtype_column_label(self):
    label = 'subtype_column_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_array_subtype_column_label(self):
    label = 'array_subtype_column_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_cit_label(self):
    label = 'class_info_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_array_cit_label(self):
    label = 'array_cit_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_create_object_function_label(self):
    label = 'create_object_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  @property
  def c_create_array_function_label(self):
    label = 'create_array_{0}'.format(self.canonical_name)
    return CodeGenManager.memoize_label(self, label)

  def c_gen_code(self):
    '''Code generation for types'''
    # Generate code for all the methods.
    methods = []
    for m in self.methods:
      methods.extend([m.c_gen_code(), ''])

    import code_gen.sit.selector_index_table as sit
    return [
      methods,
      '', '',  # Padding before the SIT/Subtype columns.
      sit.gen_code_sit_column(self.c_sit_column, self.c_sit_column_label),
      '', '',  # Padding between tables.
      self.c_gen_code_subtype_columns(),
      '', '',
      self.c_gen_code_create_instance(),
      '', '',
      self.c_gen_code_create_array(),
      '', '',
      cit.generate_array_cit(self.canonical_name, self.c_array_cit_label,
          self.c_array_sit_column_label, self.c_array_subtype_column_label),
      '', '',
      cit.generate_cit(self),  # THIS MUST BE LAST.
    ]

  def c_gen_code_subtype_columns(self):
    '''Generates assembly for the subtype table for this type'''
    # We use a helper as subtype columns for classes and interfaces are created
    # the same way.
    subtype_column_code = ASTClass.c_gen_code_subtype_column_helper(
        self.c_subtype_column_label, self.c_subtype_column)
    array_subtype_column_code = ASTClass.c_gen_code_subtype_column_helper(
        self.c_array_subtype_column_label, self.c_array_subtype_column)
    return [subtype_column_code, '', array_subtype_column_code]

  def c_calculate_field_offsets(self):
    '''Calculate the offsets for field instances'''
    # Don't bother if we've already done the calculations.
    if self.c_has_obj_offset:
      return

    # Calculate offests for the super type first, if any.
    if self.has_super:
      t_super = self.super[0].definition
      t_super.c_calculate_field_offsets()
      self.c_obj_offset = t_super.c_obj_offset

    # Order the fields so it's deterministic.
    fields = list(self.fields)
    fields.sort(key=lambda x: str(x.identifier))
    for f in fields:
      # Only assign field offsets to instance (i.e. non-static) fields.
      if not f.is_static:
        f.c_offset = self.c_obj_offset
        self.c_obj_offset += 4

    self.c_has_obj_offset = True
    return

  def c_calculate_size(self):
    '''Calculates the size for the object in bytes'''
    size = 4  # starts at 4 because of the pointer to the CIT.
    for f in self.get_all_fields():
      # Add 4 for all instance (i.e. non-static) fields.
      if not f.is_static:
        size += 4

    self.c_object_size = size

  def c_add_static_to_init(self):
    '''Add static fields to the initializtion list in CodeGenManager'''
    for f in self.fields:
      if f.is_static:
        CodeGenManager.add_static_var_to_init(self, f)
    return

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

  def c_gen_code_create_instance(self):
    '''Creates an instance of this class in memory and does all prep work so
    that the constructor can be called. Precisely, does the following:

    1. Allocate memory for the object.
    2. Sets a pointer to the CIT on the instance.
    3. Initializes all fields to their default value.

    The following should be done by the ClassInstanceCreation:
    1. Call the parent constructor.
    2. Initialize fields declared on the class.
    3. Run constructor body.'''

    import code_gen.asm.common as common
    import code_gen.asm.object as object_

    field_init_code = []
    for f in self.get_all_fields():
      type_node = f.type_node
      field_init_code.extend([
        'push eax ; save |this|',
        object_.create_default_value(type_node.is_primitive,
            type_node.is_array),
        'mov ebx, eax ; store result in ebx',
        'pop eax ; restore |this|',
        common.save_instance_field('eax', f, 'ebx'),
      ])

    return [
      'global {0}'.format(self.c_create_object_function_label),
      '{0}:'.format(self.c_create_object_function_label),
      common.malloc(self.c_object_size),
      # Class info table
      'mov dword [eax], {0}'.format(self.c_cit_label),
      field_init_code,
      'ret',
    ]

  def c_gen_code_create_array(self):
    from parser.ast.ast_type import ASTType
    type_ = ASTType.from_str(str(self.name), is_primitive=False)
    type_.definition = self
    offset = CodeGenManager.get_subtype_table_index(type_)
    return ASTClass.c_gen_code_create_array_helper(
        self.c_create_array_function_label, self.c_array_cit_label, offset)

  @staticmethod
  def c_gen_code_create_array_helper(function_label, array_cit_label, offset):
    '''Create an array of this type in memory

    Structure of the created array object is as follows:
      1. Pointer to Array CIT
      2. This type's offset into the subtype table
      3. Length (reference to a integer)
      4. Array elements

    1 Param:
      The length of the array'''
    N_PARAMS = 1

    # The first 12 bytes are for the pointer to the Array CIT, subtype offset,
    # and the length. Remaining bytes are for the array elements (4 bytes each)
    return [
      'global {0}'.format(function_label),
      '{0}:'.format(function_label),
      array.create_array(False, array_cit_label, offset)     
    ]

class ASTClassError(Exception):
  pass
