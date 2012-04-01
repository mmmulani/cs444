from manager import CodeGenManager

def initialize_static_fields():
  '''Initializes static fields'''
  ret = []
  for t, f in CodeGenManager.static_inits:
    label = '; Init for {0}.{1}'.format(t.canonical_name, f.identifier)
    code = [
      label,
      'mov dword ebx, [{0} + {1}]'.format(t.c_cit_label, f.c_offset),
      'mov dword [ebx], 0x0',
      ''
    ]
    ret.append(code)

  return ret
