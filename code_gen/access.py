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

  return [
    '; Get static var {0}'.format(f.identifier),
    'mov dword eax, [{0}]'.format(f.c_defn_label)
  ]
