import asm.common as common
import parser.ast.ast_class as ast_class
import parser.ast.ast_param as ast_param
import parser.ast.ast_variable_declaration as ast_variable_declaration

from manager import CodeGenManager

NAMES = []

def set_simple_var(decl, src):
  '''Given a variable declaration (ASTParam or ASTVariableDeclaration), stores
  the value of src in it.'''
  store_code = []
  if isinstance(decl, ast_param.ASTParam):
    # Method parameter.
    index = CodeGenManager.cur_method.c_get_param_index(decl)
    store_code = common.set_param(index, src, CodeGenManager.N_PARAMS)
  elif decl.c_parent_method is not None:
    # Local variable.
    store_code = common.save_local_var(decl, src)
  else:
    # Last remaining case is a instance field access on the enclosing type.
    if not isinstance(decl, ast_variable_declaration.ASTVariableDeclaration):
      raise Exception('Simple variable is not an instance field')

    scratch_reg = [reg for reg in ['eax', 'ebx'] if reg != src][0]

    store_code = [
      '; using {0} as scratch'.format(scratch_reg),
      'push {0} ; saving scratch'.format(scratch_reg),
      common.get_param(scratch_reg, 0, CodeGenManager.N_PARAMS),
      common.save_instance_field(scratch_reg, decl, src),
      'pop {0} ; restoring scratch'.format(scratch_reg)
    ]

  return store_code

def get_simple_var(decl):
  '''Given a declaration, return code to get the variable'''
  if isinstance(decl, ast_param.ASTParam):
    # Method param.
    index = CodeGenManager.cur_method.c_get_param_index(decl)
    return common.get_param('eax', index, CodeGenManager.N_PARAMS)
  elif decl.c_parent_method is not None:
    # Local variable.
    return common.get_local_var('eax', decl)

  # Only remaining case should be an (instance) field of the encl type.
  if not isinstance(decl, ast_variable_declaration.ASTVariableDeclaration):
    raise Exception('Invalid instance var value retrieval.')

  # "this" is always the first param from an implicit "this".
  return [
    '; Field access of implicit "this"',
    common.get_param('eax', 0, CodeGenManager.N_PARAMS),
    common.get_instance_field('eax', decl)
  ]

def get_simple_static_field(ids):
  '''Resolve a simple static field access directly off the type.
  Example: ClassName.f'''
  name, defn = ids.first_definition
  if not isinstance(defn, ast_class.ASTClass):
    raise Exception('Trying to do a static field access off non-class')

  # Find the field using the last part of the id.
  f, encl_type = defn.environment.lookup_field(ids.parts[-1])
  if f is None or not f.is_static:
    raise Exception('Invalid static field access')

  return common.get_static_field(f)

def get_field_access_from_annotation(ids, annotation):
  '''Returns code to get a instance field given ids and their annotations'''
  ret = ['; Getting (field) value of {0}'.format(ids)]

  # Resolve all parts of the ID before the final field access.
  t, code = _get_to_final(ids, annotation)
  env = t.environment
  ret.append(code)

  # The final part should be an instance field acccess.
  final_part = str(ids.parts[-1])
  f, encl_type = env.lookup_field(final_part)
  ret.extend(common.get_instance_field('eax', f))

  return ret

def _get_to_final(ids, annotation):
  '''Resolve to the final part of the identifier

  Returns (ASTType, asm_code)'''

  # Figure out where the field accesses or method invocations start.
  #   - If it's off of a static variable, e.g. ClassName.static_var.f,
  #     the annotation will start with static_var
  #   - If it's off a local variable or field, e.g. v.f, the annotation
  #     will start with v
  name, decl = annotation[0]
  t = _get_type_from_decl(decl).definition
  env = t.environment
  code = []
  if str(ids).startswith(name):
    # The first part matches the ID, which means we're going off a local var
    code = get_simple_var(decl)
  else:
    # The first part is a static variable access.
    code = common.get_static_field(decl)

  # After the start, keep doing instance field accesses off the previous
  # result.
  for name, decl in annotation[1:]:
    f, encl_type = env.lookup_field(name)
    t = f.type_node.definition
    env = t.environment
    code.extend(common.get_instance_field('eax', f))

  return t, code

def _get_type_from_decl(decl):
  '''Gets the ASTType from a declaration node

  A declaration node can be an ASTParam (method param) or an
  ASTVariableDeclaration (local or field)'''
  if isinstance(decl, ast_param.ASTParam):
    return decl.type
  elif isinstance(decl, ast_variable_declaration.ASTVariableDeclaration):
    return decl.type_node

  raise Exception('Invalid declaration type')
