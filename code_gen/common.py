NAMES = []

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

def get_param(dest, index, num_params):
  ''' Gets the (index)th parameter and stores it in dest. '''
  if index < 0 or index >= num_params:
    raise Exception('Invalid parameter index')
  offset = 8 + 4 * (num_params - (index + 1))
  return [
    'mov {0}, [ebp + {1}]'.format(dest, offset)
  ]
