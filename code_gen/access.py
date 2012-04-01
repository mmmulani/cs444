import asm.common as common 
import parser.ast.ast_class as ast_class 
import parser.ast.ast_param as ast_param
import parser.ast.ast_variable_declaration as ast_variable_declaration

NAMES = []

def get_simple_var(decl):
  '''Given a declaration, return code to get the variable'''
  if isinstance(decl, ast_param.ASTParam):
    # Method param.
    return ''
  elif decl.c_parent_method is not None:
    # Local variable.
    return common.get_local_var('eax', decl)

  # Only remaining case should be an (instance) field of the encl type.
  if not isinstance(decl, ast_variable_declaration.ASTVariableDeclaration):
    raise Exception('Invalid instance var value retrieval.')

  return ''

def get_simple_static_field(ids):
  '''Resolve a simple static field access directly off the type.
  Example: ClassName.f'''
  name, defn = ids.first_definition
  if not isinstance(defn, ast_class.ASTClass):
    raise Exception('Trying to do a static field access off non-Class')

  # Find the field using the last part of the id.
  f, encl_type = defn.environment.lookup_field(ids.parts[-1])
  if f is None or not f.is_static:
    raise Exception('Invalid static field access')

  return _get_static_field(f)

def get_field_access_from_annotation(ids, annotation):
  '''Returns code to get a instance field given ids and their annotations'''
  ret = ['; Getting (field) value of {0}'.format(ids)]

  # Figure out where the field accesses start.
  #   - If it's off of a static variable, e.g. ClassName.static_var.f,
  #     the annotation will start with static_var
  #   - If it's off a local variable or field, e.g. v.f, the annotation
  #     will start with v
  name, decl = annotation[0]
  t = decl.type_node.definition
  env = t.environment
  if str(ids).startswith(name):
    # The first part matches the ID, which means we're going off a local var
    ret.append(get_simple_var(decl))
  else:
    # The first part is a static variable access.
    # TODO: use get_simple_static_field?
    ret.append(_get_static_field(decl))

  for name, decl in annotation[1:]:
    f, encl_type = env.lookup_field(name)
    t = f.type_node.definition
    env = t.environment
    ret.extend(_get_instance_field(f))

  final_part = str(ids.parts[-1])
  f, encl_type = env.lookup_field(final_part)
  ret.extend(_get_instance_field(f))

  return ret

def _get_static_field(f):
  '''Returns code to get a static field f'''
  return [
    '; Get static var {0}'.format(f.identifier),
    'mov dword eax, [{0}]'.format(f.c_defn_label)
  ]

def _get_instance_field(f, reg='eax'):
  '''Gets the instance field off the object at reg into eax'''
  return [
    'mov eax, [{0} + {1}]'.format(reg, f.c_offset)
  ]
