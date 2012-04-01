import asm.object

from manager import CodeGenManager

def initialize_static_fields():
  '''Initializes static fields'''
  ret = []
  for t, f in CodeGenManager.static_inits:
    init = asm.object.create_starting_value(f)
    code = [
      '; --- INIT for {0}.{1} ---'.format(t.canonical_name, f.identifier),
      init,
      '; --- END INIT ---',
      'mov dword ebx, [{0} + {1}]'.format(t.c_cit_label, f.c_offset),
      'mov dword [ebx], eax',
      ''
    ]
    ret.append(code)

  return ret
