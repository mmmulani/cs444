import sys

''' Takes in an LR1 file and outputs the reduce/shift tables
  Usage:
    python build_shift_reduce_maps LR1-input-file reduce-map shift-map
'''

def main():
  assert len(sys.argv) == 4, "need 1 input file name, 2 output filenames"
  lr1_filename = sys.argv[1]
  reduce_map_filename = sys.argv[2]
  shift_map_filename = sys.argv[3]

  f = open(lr1_filename, 'r')
  lines = f.readlines()
  lines = [x.rstrip() for x in lines]  # remove newlines
  lines.reverse()  # so the start of the file is the top of the stack
  f.close()

  # read the CFG section:
  num_terminals = int(lines.pop())
  terminals = pop_n(lines, num_terminals)
  num_non_terminals = int(lines.pop())
  non_terminals = pop_n(lines, num_non_terminals)
  start_symbol = lines.pop()
  num_rules = int(lines.pop())
  rules = pop_n(lines, num_rules)

  # read the LR(1) machine section:
  num_states = int(lines.pop())
  num_transitions = int(lines.pop())
  transitions = pop_n(lines, num_transitions)

  # build the Reduce/Shift tables using the LR(1) machine transitions:
  Reduce = {}
  Shift = {}
  for trans in transitions:
    trans = trans.split(' ')
    if trans[2] == 'reduce':
      state = int(trans[0])
      terminal = trans[1]
      rule = int(trans[3])
      Reduce[(state, terminal)] = (rules[rule]).split(' ')
    elif trans[2] == 'shift':
      state_1 = int(trans[0])
      symbol = trans[1]
      state_2 = int(trans[3])
      Shift[(state_1, symbol)] = state_2
    else:
      raise Exception('Error: transition must be reduce or shift')

  # output the Reduce/Shift tables:
  f = open(reduce_map_filename, 'w')
  f.write(str(Reduce))
  f.close()
  f = open(shift_map_filename, 'w')
  f.write(str(Shift))
  f.close()


def pop_n(stack, n):
  ret = []
  for i in range(0,n):
    ret.append(stack.pop())
  return ret


if __name__ == '__main__':
  main()
