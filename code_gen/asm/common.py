def function_prologue(frame_size=0):
  ''' The code that should be at the start of every function. '''
  return [
    '; FUNCTION PROLOGUE --------------',
    'push ebp  ; save original frame pointer',
    'mov ebp, esp  ; move stack pointer into frame pointer',
    'sub esp, {0}  ; move stack pointer up for frame'.format(frame_size),
    '; save all registers (except eax)',
    # we dont push eax because it will contain the return value
    'push ebx',
    'push ecx',
    'push edx',
    'push esi',
    'push edi',
    '; END FUNCTION PROLOGUE ----------'
  ]

def function_epilogue():
  ''' The code that should be at the end of every function. '''
  return [
   '; FUNCTION EPILOGUE --------------',
   'pop edi',
   'pop esi',
   'pop edx',
   'pop ecx',
   'pop ebx',
   'mov esp, ebp  ; restore original stack pointer',
   'pop ebp  ; restore original frame pointer',
   'ret',
   '; END FUNCTION EPILOGUE ----------'
  ]

def malloc(n_bytes):
  ''' Calls malloc to get n_bytes of memory.
  The address of the allocated memory will be put in eax.
  The number of bytes allocated must be a multiple of 4. '''

  if n_bytes % 4 != 0:
    raise Exception('Number of bytes given to malloc must be multiple of 4')

  return [
    'mov eax, {0}'.format(n_bytes),
    'call __malloc'
  ]

def malloc_reg(src):
  ''' Calls malloc, using the value in the src register as the number of
  bytes to allocate '''
  return [
    'mov eax, {0}'.format(src),
    'call __malloc'
  ]

def get_param(dest, index, num_params):
  ''' Gets the (index)th parameter and stores it in dest. '''
  if index < 0 or index >= num_params:
    raise Exception('Invalid parameter index')
  offset = 8 + 4 * (num_params - (index + 1))
  return [
    'mov {0}, [ebp + {1}]'.format(dest, offset)
  ]

def set_param(index, src, num_params):
  '''Stores the value from src in the (index)th parameter.'''
  if index < 0 or index >= num_params:
    raise Exception('Invalid parameter index')

  offset = 8 + 4 * (num_params - (index + 1))
  return [
    'mov [ebp + {0}], {1}'.format(offset, src)
  ]

def get_local_var(dest, local_var):
  '''Takes an ASTVariableDeclaration and stores the pointer to its data in
  dest.'''
  index = local_var.c_method_frame_index
  if index < 0:
    raise Exception('Local variable does not appear on the stack')

  offset = (index + 1) * 4

  return ['mov {0}, [ebp - {1}]'.format(dest, offset)]

def save_local_var(local_var, src):
  '''Takes an ASTVariableDeclaration and a register and replaces the value on
  the stack corresponding to the variable declaration.'''
  index = local_var.c_method_frame_index
  if index < 0:
    raise Exception('Local variable does not appear on the stack')

  offset = (index + 1) * 4

  if src != 'eax':
    scratch_reg = 'eax'
  else:
    scratch_reg = 'ebx'

  return [
    '; using {0} as scratch'.format(scratch_reg),
    'push {0}'.format(scratch_reg),
    'mov {0}, ebp'.format(scratch_reg),
    'sub {0}, {1}'.format(scratch_reg, offset),
    'mov [{0}], {1}'.format(scratch_reg, src),
    'pop {0}'.format(scratch_reg),
    '; phew. no longer using {0} as scratch'.format(scratch_reg),
  ]

def save_instance_field(this_reg, field_decl, src):
  '''Stores a value into the field of a class instance.
  this_reg is a register that points to the class instance.
  field_decl is the ASTVariableDeclaration for instance field.
  src is a register whose value will be stored in the field.'''

  offset = field_decl.c_offset
  if offset is None:
    raise Exception('Instance field does not have an offset')

  if src == this_reg:
    raise Exception('Warning: saving |this| as instance field on object')

  return [
    check_null(this_reg),
    'mov [{0} + {1}], {2}'.format(this_reg, offset, src),
  ]

def get_instance_field(this_reg, dest, field_decl):
  '''Gets the instance field out of this_reg'''
  offset = field_decl.c_offset
  if offset is None:
    raise Exception('Instance field does not have an offset')

  return [
    check_null(this_reg),
    'mov {0}, [{1} + {2}]'.format(dest, this_reg, offset)
  ]

def check_null(src):
  '''Checks whether the value in src is null (0x0).'''
  from code_gen.manager import CodeGenManager
  check_pass = CodeGenManager.get_label('null_check_pass');
  return [
    'cmp {0}, 0'.format(src),
    'jne {0}'.format(check_pass),
    'call __exception',
    '{0}:'.format(check_pass)
  ]

def get_instance_field_addr(this_reg, dest, field_decl):
  '''Gets the instance field address out of this_reg'''
  offset = field_decl.c_offset
  if offset is None:
    raise Exception('Instance field does not have an offset')

  return [
    check_null(this_reg),
    '; Get instance field addr',
    'mov {0}, {1}'.format(dest, this_reg),
    'add {0}, {1}'.format(dest, offset)
  ]

def set_static_field(field_decl, src):
  return [
    '; Set static var {0}'.format(field_decl.identifier),
    'mov dword [{0}], {1}'.format(field_decl.c_defn_label, src)
  ]

def get_static_field(dest, field_decl):
  '''Gets the static field in field_decl and puts it in dest'''
  return [
    '; Get static var {0}'.format(field_decl.identifier),
    'mov dword {0}, [{1}]'.format(dest, field_decl.c_defn_label)
  ]

def get_array_length(dest, src):
  '''Gets the array length of the array object in src and puts it in dest'''
  return [
    'mov {0}, [{1} + 8]  ; Get array length'.format(dest, src)
  ]

def invoke_instance_method(this_reg, m, args_asm):
  '''Invokes an instance method m off this_reg'''
  if m.c_offset is None:
    raise Exception('Instance method has no offset')

  n_params = len(m.params)
  pop_asm = ['pop ebx ; Pop param to garbage' for x in range(m.c_num_params)]

  return [
    '; Invoke instance method: {0}'.format(m.name),
    check_null(this_reg),
    'push {0}  ; push "this" as the first param'.format(this_reg),
    args_asm,
    'mov dword eax, [esp + 4*{0}]  ; Get to "this"'.format(n_params),
    'mov dword eax, [eax]  ; Get to CIT',
    'mov dword eax, [eax + {0}]  ; Get the method'.format(m.c_offset),
    'call eax  ; Call the method',
    pop_asm,
  ]

def invoke_interface_method(this_reg, m, args_asm):
  '''Invokes an interface method m off this_reg using the SIT'''
  from code_gen.manager import CodeGenManager

  offset = CodeGenManager.get_sit_offset(m)
  n_params = len(m.params)
  pop_asm = ['pop ebx ; Pop param to garbage' for x in range(m.c_num_params)]

  return [
    '; Invoke interface method: {0}'.format(m.name),
    check_null('eax'),
    'push eax  ; Push "this" as the first param',
    args_asm,
    'mov dword eax, [esp + 4*{0}]  ; Get to "this"'.format(n_params),
    'mov dword eax, [eax]  ; Get to CIT for T[]',
    'mov eax, [eax]  ; Get to SIT for T[]',
    'mov eax, [eax + {0}]  ; Get the method loc in the SIT'.format(offset),
    'call eax  ; Call the method',
    pop_asm,
  ]

def invoke_static_method(t, m, args_asm):
  '''Invokes a static method m on type t'''
  if t is None:
    raise Exception('Calling static method with no type')

  if m.c_offset is None:
    raise Exception('Calling static method with no offset')

  # Native method. Only used for java.io.OutputStream.
  if 'native' in m.modifiers:
    return [
      '; Invoke static method: java.io.OutputStream.nativeWrite',
      args_asm,
      'pop eax ; put param into eax',
      unwrap_primitive('eax', 'eax'),
      'call NATIVEjava.io.OutputStream.nativeWrite',
      'push eax ; create_int out of return type',
      'call _create_int',
      'pop ebx',
    ]

  pop_asm = ['pop ebx ; Pop param to garbage' for x in range(m.c_num_params)]

  return [
    '; Invoke static method: {0}'.format(m.name),
    args_asm,
    'mov dword eax, {0}  ; Get to the CIT'.format(t.c_cit_label),
    'mov dword eax, [eax + {0}]  ; Get method defn'.format(m.c_offset),
    'call eax  ; Call the method',
    pop_asm,
  ]

def unwrap_primitive(dest, src):
  '''Unwraps the primitive at *src and stores it in the register dest.'''
  return 'mov {0}, [{1}]'.format(dest, src)

def unwrap_cit(dest, src):
  '''Given an object in src, stores a pointer to the CIT in dest.'''
  return 'mov {0}, [{1}]'.format(dest, src)

def unwrap_subtype_col_from_object(dest, src):
  '''Given an object in src, stores a pointer to the subtype column in dest.'''
  return [
    unwrap_cit(dest, src),
    'mov {0}, [{0} + 4]'.format(dest, dest),
  ]

def store_param(ast_node):
  '''Pushes the value of the ast node on to the stack to be used as a param'''
  return [
    ast_node.c_gen_code(),
    'push eax ; Push result as a paramater'
  ]

def fill_high_order_bit(src, dest):
  '''Fill a dest register with the high order bit of the src register'''
  return [
    '; Fill {0} with high order bit by copying then shifting'.format(dest),
    'mov {0}, {1}'.format(dest, src),
    'sar {0}, 31  ; Arithmetic right shift 31 positions'.format(dest)
  ]

def if_false(ast_node, label):
  '''Computes the value of the ast node and if it is false, branches to label.
  This expects the value of ast_node to be a boolean. A reference to the boolean
  value is left in eax.'''
  return [
    ast_node.c_gen_code(),
    unwrap_primitive('ebx', 'eax'),
    'mov ecx, 0',
    'cmp ebx, ecx',
    'je {0}'.format(label),
  ]

def if_true(ast_node, label):
  '''Computes the value of the ast node and if it is true, branches to label.
  This expects the value of ast_node to be a boolean. A reference to the boolean
  value is left in eax.'''
  return [
    ast_node.c_gen_code(),
    unwrap_primitive('ebx', 'eax'),
    'mov ecx, 1',
    'cmp ebx, ecx',
    'je {0}'.format(label),
  ]

def sys_exit(src):
  '''Code used to exit the program (by making a system call). src should
  contain the program's exit code.'''
  return [
    '; Get the int value returned',
    unwrap_primitive('eax', 'eax'),
    '; Put the program return value in ebx',
    'mov ebx, {0}'.format(src),
    '; Load 1 into eax to indicate sys_exit',
    'mov eax, 1',
    '; Exit!',
    'int 0x80'
  ]

NAMES = {}
