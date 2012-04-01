import asm.object
import asm.common as common

from manager import CodeGenManager

def initialize_static_fields():
  '''Initializes static fields'''
  ret = []
  # First set default values.
  for t, f in CodeGenManager.static_inits:
    init = asm.object.create_default_value(f)
    code = [
      '; --- Default init for {0}.{1}'.format(t.canonical_name, f.identifier),
      init,
      common.set_static_field(f, 'eax'),
      '',
    ]
    ret.append(code)

  # Next we set all fields that have an explicit initialization expression.
  for t, f in CodeGenManager.static_inits:
    if f.expression is None:
      continue

    init = asm.object.create_starting_value(f)
    code = [
      '; --- INIT for {0}.{1} ---'.format(t.canonical_name, f.identifier),
      init,
      '; --- END INIT ---',
      common.set_static_field(f, 'eax'),
      ''
    ]
    ret.append(code)

  return ret
