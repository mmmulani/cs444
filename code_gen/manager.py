class CodeGenManager(object):
  '''Static class that acts as a global singleton for code generation.'''
  def __init__(self):
    # This should be a static class only.
    raise Exception('Code generation manager is a static global singleton.')

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
