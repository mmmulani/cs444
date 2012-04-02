import access
import annotate_ids
import asm.common as common
import parser.ast.ast_interface as ast_interface
import parser.ast.ast_class as ast_class

from manager import CodeGenManager

def call_simple_method(ids, arg_types, args_asm):
  '''Invoke a simple method name from an identifier.'''
  annotation = annotate_ids.annotate_identifier(ids)

  t, code = access._get_to_final(ids, annotation)
  return call_method_with_final(t.definition, ids, code, arg_types, args_asm)

def call_method_with_final(t, ids, code, arg_types, args_asm):
  '''Calls the method off t using the final part of the identifier'''

  ret = ['; Simple method invocation: {0}()'.format(ids)]
  env = t.environment
  ret.append(code)

  # Invoke a method using the final part.
  final_part = str(ids.parts[-1])

  # Invoke class instance or static method.
  m, encl_type = env.lookup_method((final_part, arg_types))
  if m is None:
    raise Exception('Trying to invoke non-existant method')

  if isinstance(t, ast_interface.ASTInterface):
    # Use the SIT table for interface methods.  Interfaces can not have
    # static methods.
    ret.append(common.invoke_interface_method('eax', m, args_asm))
  else:
    ret.append(common.invoke_instance_method('eax', m, args_asm))

  return ret 

def call_method_parts(t, ids, arg_types, arg_asm):
  '''Calls a method starting from a type followed by a list of IDs

  ex. (Foo.static_field.field).field.method()
  t <= typeof(Foo.static_field.field)
  ids <= field, method'''
  annotation = annotate_ids.annotate_from_type(t, ids.parts)
  t, code = access._get_to_final_from_type(t, annotation, [])

  return call_method_with_final(t.definition, ids, code, arg_types, arg_asm)

def call_static_method(ids, arg_types, args_asm):
  '''Call a static method Type.m off the identifiers'''
  name, defn = ids.first_definition
  if not isinstance(defn, ast_class.ASTClass):
    raise Exception('Trying to do static method invocation on non-Class')

  m, encl_type = defn.environment.lookup_method((ids.parts[-1], arg_types))
  if m is None or not m.is_static:
    raise Exception('Invalid static method invocation')

  return common.invoke_static_method(defn, m, args_asm)

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
