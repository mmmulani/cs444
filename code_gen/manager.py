class CodeGenManager(object):
  '''Static class that acts as a global singleton for code generation.'''
  def __init__(self):
    # This should be a static class only.
    raise Exception('Code generation manager is a static global singleton.')

  _label_count = 0

  @staticmethod
  def get_labels(*args):
    '''Get a set of labels with a unique prefix attached to the end of them

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
