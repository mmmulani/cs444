import parser.ast.ast_interface as ast_interface

def calc_offset(ast):
  '''Calculates the offsets for the enclosing class in the ASTRoot, if any'''
  if ast.class_or_interface:
    # We don't need to do any offset calculations for interfaces.
    # TODO: Is this always true?
    if isinstance(ast.class_or_interface, ast_interface.ASTInterface):
      return
    calc_offset_from_defn(ast.class_or_interface)

  return

def calc_offset_from_defn(t):
  '''Calculate the offsets for all the methods in a class t'''
  # TODO: This should probably do fields at some point too.

  # If our offsets have been calculated before, don't bother recalculating.
  if t.c_has_offset:
    return

  # Calculate the offsets in any super class first, and update the offset
  # of this type so that we can continue to grow the list, if necessary.
  if t.has_super:
    # Super is a list to match ASTInterface, but classes can only ever
    # extend one type.
    supertype = t.super[0].definition
    calc_offset_from_defn(supertype)
    t.c_max_offset = supertype.c_max_offset

  env = t.environment
  for m in t.methods:
    offset = _get_inherited_offset(t, m)
    if offset is not None:
      # Method is overriding something from the parent. Use the offset given.
      m.c_offset = offset
    else:
      # The method is new, so create an offset for it.
      m.c_offset = t.c_max_offset
      t.c_max_offset += 4

  # Set the has_offset flag so we don't need to recalculate.
  t.c_has_offset = True
  return

def _get_inherited_offset(t, m):
  '''Returns an offset for an overridden method m defined in type t

  If no such method is found, return None.'''
  if not t.has_super:
    return None

  supertype = t.super[0].definition

  for sig, super_m in supertype.get_all_methods():
    if super_m.signature == m.signature:
      # If the super method was from an interface, it's offset will be
      # None, which is what we'll want to return anyway.
      return super_m.c_offset
  return None
