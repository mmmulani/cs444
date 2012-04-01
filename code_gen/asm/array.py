import code_gen.asm.object as asm_object
import code_gen.asm.common as common

from code_gen.manager import CodeGenManager

def create_array(is_primitive, cit_label, array_cit_label = 0):
  ''' Returns code for a function that creates an array in memory.
  This function does NOT include a label, because each reference/primitive
  type will need their own version of this function. You should put your
  own label above this code.

  Structure of the created array object is as follows:
    1. Pointer to Array CIT
    2. Pointer to (regular) CIT for reference types, null for primitives
    3. Length (reference to a integer)
    4. Array elements

  1 Param:
    The length of the array (a reference to an integer)'''
  N_PARAMS = 1

  # The first 12 bytes are for the pointer to the Array CIT, the regular CIT,
  # and the length. Remaining bytes are for the array elements (4 bytes each)

  return [
    common.function_prologue(),
    common.get_param('ebx', 0, N_PARAMS),
    common.unwrap_primitive('ebx', 'ebx'),
    '; ebx now contains the length of the array',
    'push ebx  ; store the array length (# elems)',
    '; calculate how much memory to allocate, based on length of array:',
    'imul ebx, 4  ; 4 bytes for every element',
    'add ebx, 12  ; add an extra 12 bytes for pointers/length field',
    common.malloc_reg('ebx'),
    'pop ebx  ; restore length (# elems)',
    'mov edx, eax  ; save pointer to array memory in edx', 
    'push eax',
    '; set array elems to their default values:',
    _array_init_loop(is_primitive),
    '; create an int to store the length of the array:',
    'push ebx;',
    'call _create_int',
    'pop ecx; pop param to garbage',
    'mov ebx, eax  ; ebx has pointer to integer representing array length',
    'pop eax  ; eax now has pointer to memory from malloc call',
    'mov dword [eax], {0}'.format(array_cit_label),
    'mov dword [eax + 4], {0}'.format(cit_label),
    'mov dword [eax + 8], ebx',
    common.function_epilogue()
  ]

def _array_init_loop(is_primitive):
  ''' Code that loops through array elements to initialize them.
  This code does not save/restore registers, it should only be called from
  create_array() '''
  
  # Code that will create the default value for a single array element:
  default_value_code = asm_object.create_default_value(is_primitive)

  loop_start, loop_end = CodeGenManager.get_labels(
    'array_init_loop_start', 'array_init_loop_end')
  
  # eax gets set to the an element'ss default value
  # ebx stores the length of the array (number of elements)
  # ecx is the loop counter
  # edx is a pointer to the start of the array
  return [
    'mov ecx, 0  ; ecx is counter for which array index we\'re at',
    '{0}:'.format(loop_start),
    'cmp ecx, ebx  ; loop condition (check if done all array elements)',
    'je {0}'.format(loop_end),
    '; init current array elem to default value:',
    default_value_code,
    'mov [edx + 12 + 4*ecx], eax',
    'add ecx, 1  ; increment loop counter',
    'jmp {0}'.format(loop_start),
    '{0}:'.format(loop_end),
  ]

NAMES = {}
