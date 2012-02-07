from tree_node import TreeNode

class Parser(object):
  '''Parser object
  Takes a list of tokens, and returns a parse tree if the tokens can be
  successfully parsed (otherwise, an exception is thrown)
  '''

  def __init__(self, reduce_filename = "reduce_table", 
               shift_filename = "shift_table"):
    self.reduce_filename = reduce_filename
    self.shift_filename = shift_filename

  def parse(self, tokens):
    reduce_file = open(self.reduce_filename, "r")
    shift_file = open(self.shift_filename, "r")
    Reduce = eval(reduce_file.read())
    Shift = eval(shift_file.read())
    reduce_file.close()
    shift_file.close()
    
    node_stack = []
    state_stack = [0]
    for i in range(0, len(tokens)):
      token = tokens[i]
      reduction = Reduce.get((state_stack[-1], token), None)
      while reduction is not None:
        # reduction is a list of symbols, where the first symbol is the LHS
        # of a reduction rule, and the remaining sybols are the RHS of the rule
        LHS = reduction[0]
        RHS = reduction[1:]

        child_tokens = []
        # pop once for every token on the RHS of the reduction rule:
        for i in range(0,len(RHS)):
          child_tokens.append(node_stack.pop())
          state_stack.pop()

        child_tokens.reverse()
        node_stack.append(TreeNode(LHS, child_tokens))
        state_stack.append(Shift[(state_stack[-1], LHS)])
          
        reduction = Reduce.get((state_stack[-1], token), None)

      # we couldn't reduce, so try a shift:
      node_stack.append(TreeNode(token))
      shift = Shift.get((state_stack[-1], token), None)
      if shift == None:
        self._debug_output(tokens, i, node_stack)
        raise Exception('Parsing error!')
      state_stack.append(shift)

    # TODO (gnleece) is parse tree always between BOF and EOF?
    assert(len(node_stack) == 3)
    return node_stack[1]

  def _debug_output(self, tokens, i, node_stack):
    print "Tokens processed:"
    print tokens[:i]
    print "\nTokens remaining:"
    print tokens[i:]
    print "\nTree stack:"
    for tree in node_stack:
      tree.debug_print()
      print "------"
