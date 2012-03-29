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
    method, defn = env.lookup_method_inherited(m.signature, m.is_constructor)
    if method:
      # Method came from a parent.  If it's not from an interface (which is
      # handled by the SIT table), then use the offset on the overriden method.
      if not isinstance(defn, ast_interface.ASTInterface):
        # TODO: assert that method.c_offset is not None, maybe?
        m.c_offset = method.c_offset
    else:
      # Method is new, so create an offset for it.
      m.c_offset = t.c_max_offset
      t.c_max_offset += 4

  # Set the has_offset flag so we don't need to recalculate.
  t.c_has_offset = True
  return
