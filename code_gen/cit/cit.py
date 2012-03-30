def generate_cit(t):
  '''Generates the Class Info Table (CIT) column from an ASTClass

  Class Info Table:
      - Pointer to SIT column
      - Pointer to Subtype column
      - Static fields and methods (remembering inheritance order)
  '''

  # TODO: assert t.c_has_offset == True here, maybe?
  method_impls = _get_method_offsets(t)

  return [
    '; CLASS INFO TABLE: {0}'.format(t.canonical_name),
    '{0}:'.format(t.c_class_info_table_label),
    'dd {0}'.format(t.c_sit_column_label),
    'dd {0}'.format(t.c_subtype_column_label),
    method_impls
  ]

def _get_method_offsets(t):
  '''Returns a list of pointers to the method implementations for the type'''
  offset_impl_list = []
  for sig, m in t.get_all_methods():
    # If no offset has been set for the method, then this method was defined
    # on an interface and we will resolve it later using the SIT.
    if m.c_offset is None:
      continue

    # Offsets should be dword aligned.
    if m.c_offset % 4 != 0:
      raise Exception('Offset for {0} is not a multiple of 4'.format(m.name))

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
