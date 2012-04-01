class CodeGenManager(object):
  '''Static class that acts as a global singleton for code generation.'''
  def __init__(self):
    # This should be a static class only.
    raise Exception('Code generation manager is a static global singleton.')

  found_start_method = False
  java_lang_object_defn = None

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

  # A mapping from canonical names -> names that need to be externed
  # in other files.
  global_labels_map = {}

  @staticmethod
  def add_global_label(k, v):
    if k in CodeGenManager.global_labels_map.keys():
      CodeGenManager.global_labels_map[k].append(v)
    else:
      CodeGenManager.global_labels_map[k] = [v]

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

  # ------- STATIC FIELD INIT METHODS ------
  # A list of (ASTClass, ASTVariableDeclaration) pairs of static fields
  # that need to be initialized.
  #   - ASTClass will be the type defining the static field
  #   - ASTVariableDeclaration will be the declaration of the static field
  static_inits = []

  @staticmethod
  def add_static_var_to_init(t, f):
    CodeGenManager.static_inits.append((t, f))
