import asm.common as common

from manager import CodeGenManager
from parser.ast.ast_type import ASTType

def string_concat(bin_expr):
  '''Generate code to concat two string in a ASTBinary'''
  left = bin_expr.left_expr
  right = bin_expr.right_expr

  left_asm = left.c_gen_code()
  right_asm = right.c_gen_code()

  # We want to call valueOf on the left and right regardless of their type as
  # valueOf handles the case where left or right is null.
  m = _get_valueof_method_from_type(left.expr_type)
  left_convert_asm = [
    '; Convert the left value to a string',
    left_asm,
    '; Left value in eax',
    'push eax  ; push value as param',
    'call {0}  ; call valueOf'.format(m.c_defn_label),
    'pop ebx  ; pop param',
    '; A pointer to a String is in eax',
  ]

  m = _get_valueof_method_from_type(right.expr_type)
  right_convert_asm = [
    '; Convert the right value to a string',
    right_asm,
    '; Right value in eax',
    'push eax  ; push value as param',
    'call {0}  ; call valueOf'.format(m.c_defn_label),
    'pop ebx  ; pop param',
    '; A pointer to a String is in eax',
  ]

  concat_m = _get_concat_method_from_obj()

  # The String on the right is the paramater to the method, so it must
  # be pushed on the stack.
  return [
    left_convert_asm,
    'push eax  ; push left',
    right_convert_asm,
    'push eax  ; push right',
    'call {0}  ; call concat'.format(concat_m.c_defn_label),
    'pop ebx  ; pop to ether',
    'pop ebx  ; pop to ether',
  ]
  
def _is_expr_type_string(t):
  '''Checks if an expr_type property is java.lang.String'''
  return (t.definition == CodeGenManager.java_lang_string_defn)

def _get_valueof_method_from_type(t):
  '''Gets the method for String's valueOf method given the param type'''
  env = CodeGenManager.java_lang_string_defn.environment
  param_t = t
  if not t.is_primitive or t.is_array or t == ASTType.ASTNull:
    return CodeGenManager.java_lang_string_defn.methods[10]

  m, encl_type = env.lookup_method(('valueOf', [t]))
  if m is None:
    raise Exception('No valueOf method found for type {0}.'.format(t))

  return m

def _get_concat_method_from_obj():
  '''Gets the method for String's concat method given the param type'''
  env = CodeGenManager.java_lang_string_defn.environment
  m, encl_type = env.lookup_method(('concat', [ASTType.ASTString]))
  if m is None:
    raise Exception('No concat method found!');

  return m
