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
    if CodeGenManager._has_tag(k):
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
