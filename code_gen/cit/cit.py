from code_gen.manager import CodeGenManager

def generate_cit(t):
  '''Generates the Class Info Table (CIT) column from an ASTClass

  Class Info Table:
      - Pointer to SIT column
      - Pointer to Subtype column
      - Static fields and methods (remembering inheritance order)
  '''
  if not t.c_has_cit_offset:
    raise Exception(
        'Trying to generate CIT from {0} with no offsets set.'.format(t.name))

  method_and_field_impls = _get_offsets(t)
  field_defn = _get_field_defns(t)

  return [
    '; CLASS INFO TABLE: {0}'.format(t.canonical_name),
    'global {0}'.format(t.c_cit_label),
    '{0}:'.format(t.c_cit_label),
    'dd {0}'.format(t.c_sit_column_label),
    'dd {0}'.format(t.c_subtype_column_label),
    method_and_field_impls,
    '', '',
    'section .data',
    field_defn
  ]

def generate_array_cit(name, array_cit_label, array_sit_column_label,
    array_subtype_column_label):
  '''Generates the array version of the Class Info Table (CIT) column from an
  ASTClass.

  Array Class Info Table:
      - Pointer to SIT column (which is always java.lang.Object's SIT column)
      - Pointer to Subtype column
      - Methods (which all come directly from java.lang.Object)
  '''

  # the only methods defined on arrays are those from java.lang.Object:
  method_impls = _get_offsets(CodeGenManager.java_lang_object_defn)

  return [
    '; ARRAY CLASS INFO TABLE: {0}'.format(name),
    'global {0}'.format(array_cit_label),
    '{0}:'.format(array_cit_label),
    'dd {0}'.format(array_sit_column_label),
    'dd {0}'.format(array_subtype_column_label),
    method_impls
  ]

def _get_offsets(t):
  '''Returns a list of pointers to the method implementations for the type'''
  offset_impl_list = []
  for f in t.get_all_fields():
    if f.is_static:
      offset = f.c_offset
      # Check that an offset exists.
      if offset is None:
        raise Exception('Static field has no offset')

      _offset_check(offset)

      row = 'dd {0} ; Storage for static field {1}'.format(
          f.c_defn_label, f.identifier)
      offset_impl_list.append((offset, row))

  for sig, m in t.get_all_methods():
    # If no offset has been set for the method, then this method was defined
    # on an interface and we will resolve it later using the SIT.
    if m.c_offset is None:
      continue

    _offset_check(m.c_offset)

    row = 'dd {0}'.format(m.c_defn_label)
    offset_impl_list.append((m.c_offset, row))

  # Sort the list in offset order.
  offset_impl_list.sort(key=lambda x: x[0])

  # Check the offsets form a contiguous sequence.
  k = 8
  for offset, row in offset_impl_list:
    if offset != k:
      raise Exception('Gap in CIT methods at {0}'.format(row))
    k += 4

  return [row for offset, row in offset_impl_list]

def _offset_check(offset):
  '''Run all checks for an offset on the CIT'''

  # Offets should be dword aligned.
  if offset % 4 != 0:
    raise Exception('Offset for {0} is not a multiple of 4'.format(m.name))

def _get_field_defns(t):
  '''Return stoarge locations for each of the static fields.
  Static fields are stored in the data segment with code.'''
  ret = []
  for f in t.fields:
    if f.is_static:
      CodeGenManager.add_global_label(t.canonical_name, f.c_defn_label)
      ret.append([
        'global {0}'.format(f.c_defn_label),
        '{0}: ; Static field {1}'.format(f.c_defn_label, f.identifier),
        'dd 0x0',
      ])
  return ret
