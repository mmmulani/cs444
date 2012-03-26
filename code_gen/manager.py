class CodeGenManager(object):
  '''Static class that acts as a global singleton for code generation.'''
  def __init__(self):
    # This should be a static class only.
    raise Exception('Code generation manager is a static global singleton.')

  found_start_method = False

# ------ LABEL METHODS -------
  _label_count = 0

  @staticmethod
  def get_label(prefix):
    '''Get a label with a unique suffix attached to the end. Uses
    CodeGenManager.get_labels() internally.'''
    suffix, = CodeGenManager.get_labels(prefix)
    return suffix

  @staticmethod
  def get_labels(*args):
    '''Get a set of labels with a unique suffix attached to the end of them

    Example usage:
      >> if_label, else_label = CodeGenManager.get_labels('if', 'then')
      >> if_label
      if_1
      >> else_label
      else_1
      >> if_label, else_label = CodeGenManager.get_labels('if', 'then')
      >> if_label
      if_2
      >> else_label
      else_2
    '''

    CodeGenManager._label_count += 1
    return tuple(
        ['{0}_{1}'.format(x, CodeGenManager._label_count) for x in args])

  _memoized_labels = {}
  @staticmethod
  def memoize_label(hashable, label):
    '''Get a unique label for the hashable object. It is automatically
    memoized, so that the same label is returned for instance of hashable.

    Example usage:
      (inside ASTClass instance method)
      >> column_label = CodeGenManager.memoize_label(self, 'class_col')
      >> column_label
      class_col_1
      >> CodeGenManager.memoize_label(self, 'class_col')
      class_col_1
    '''
    index = (hashable, label)
    if index not in CodeGenManager._memoized_labels:
      # Cache miss! Create a unique label and store it.
      unique_label = CodeGenManager.get_label(label)
      CodeGenManager._memoized_labels[index] = unique_label

    return CodeGenManager._memoized_labels[index]

# ------ SIT METHODS -------

  _sit_column_guide = []
  @staticmethod
  def get_selector_id(selector):
    matched_ids = [i for (i, sel) in CodeGenManager._sit_column_guide if
      sel == selector]

    if len(matched_ids) != 1:
      raise Exception('Lookup for id in SIT failed.')

    return matched_ids[0]

  @staticmethod
  def get_selector(id_):
    matched_sels = [sel for (i, sel) in CodeGenManager._sit_column_guide if
        i == id_]

    if len(matched_sels) != 1:
      raise Exception('Lookup for selector in SIT failed.')

    return matched_sels[0]

# ------ TYPE TAGGING -------
  tag_map = {
    'boolean': 1,
    'byte': 2,
    'char': 3,
    'int': 4,
    'null': 5,
    'short': 6
  }
  _tag_count = 6

  @staticmethod
  def add_tag(ast_type):
    '''Adds a tag to the tag_map given an AST type

    Returns the tag value.'''
    k = CodeGenManager._type_to_str(ast_type)
    if CodeGenManager._has_tag(k):
      raise Exception('Trying to insert duplicate type tag {0}.'.format(k))

    CodeGenManager._tag_count += 1
    tag = CodeGenManager._tag_count
    CodeGenManager.tag_map[k] = tag

    return tag

  @staticmethod
  def has_tag(ast_type):
    '''Checks whether a tag exists for an AST type in the map'''
    return CodeGenManager._has_tag(CodeGenManager._type_to_str(ast_type))

  @staticmethod
  def get_tag(ast_type):
    '''Gets the tag of an AST type'''
    k = CodeGenManager._type_to_str(ast_type)
    if not CodeGenManager._has_tag(k):
      raise Exception(
          'Trying to get a tag for type {0} that does not exist.'.format(k))

    return CodeGenManager.tag_map[k]

  @staticmethod
  def _has_tag(type_str):
    '''Checks whether a tag exists for a type string (i.e. key) in the map'''
    return CodeGenManager.tag_map.has_key(type_str)

  @staticmethod
  def _type_to_str(ast_type):
    '''Convert the AST type to a string to use as a key for tag_map'''
    ret = ''
    if ast_type.is_primitive:
      ret = str(ast_type)
    else:
      ret = ast_type.definition.canonical_name

    # Array types end in "[]"
    if ast_type.is_array:
      ret += '[]'

    return ret

# ------ SUBTYPE TABLE METHODS ------
  _subtype_column_guide = []

  @staticmethod
  def get_subtype_table_index(type_):
    matched_is = [i for (i, t) in CodeGenManager._subtype_column_guide if
        t == type_]

    if len(matched_is) != 1:
      raise Exception('Lookup for type in subtype table failed.')

    return matched_is[0]

  @staticmethod
  def get_subtype_table_type(ix):
    matched_types = [t for (i, t) in CodeGenManager._subtype_column_guide if
        i == ix]

    if len(matched_types) != 1:
      raise Exception('Lookup for index in subtype table failed.')

    return matched_types[0]
