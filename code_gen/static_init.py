from manager import CodeGenManager

def initialize_static_fields():
  '''Initializes static fields'''
  ret = []
  for t, f in CodeGenManager.static_inits:
    label = '; Init for {0}.{1}'.format(t.canonical_name, f.identifier)
    code = [
      label,
      'mov dword [{0} + {1}], 0'.format(t.c_cit_label, f.c_offset),
      ''
    ]
    ret.append(code)

  return ret
