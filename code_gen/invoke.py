import access
import annotate_ids
import asm.common as common
import parser.ast.ast_interface as ast_interface

def call_simple_method(ids, arg_types, args_asm):
  '''Invoke a simple method name from an identifier.'''
  ret = ['; Simple method invocation: {0}()'.format(ids)]
  annotation = annotate_ids.annotate_identifier(ids)

  t, code = access._get_to_final(ids, annotation)
  if t.is_array:
    return ''
  env = t.definition.environment
  ret.append(code)

  if isinstance(t.definition, ast_interface.ASTInterface):
    # Use the SIT table for interface methods.
    return ''

  # Invoke class instance or static method.
  final_part = str(ids.parts[-1])
  m, encl_type = env.lookup_method((final_part, arg_types))
  if m is None:
    raise Exception('Trying to invoke non-existant method')

  if m.is_static:
    # Call a static method
    return ''
  else:
    ret.append(common.invoke_instance_method('eax', m, args_asm))

  return ret 

def get_arg_list(args):
  '''Get the code to push a list of arguments onto the stack'''
  ret = ['; --- ARG LIST ---']
  for arg in args:
    ret.append([
      arg.c_gen_code(),  # Places arg value into eax
      'push eax'
    ])
  ret.append('; --- ARG LIST END ---')

  return ret
