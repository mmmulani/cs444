class Parser(object):
  '''Parser object
  Takes a list of tokens, and returns a parse tree if the tokens can be
  successfully parsed (otherwise, an exception is thrown)
  '''

  def parse(self, tokens):
    node_stack = [TreeNode("$")]
    state_stack = []
    for token in tokens:
     reduction = Reduce(state_stack[-1], token)
     while reduction is not None:
        # Reduce should return some CFG rule, which is a list of symbols
        # where the first symbol is the LHS and the remaining ones are the RHS
        LHS = reduction[0]
        RHS = reduction[1:]
        child_tokens = []

        # pop once for every token on the RHS of the reduction rule:
        for i in range(0,len(RHS)):
          child_tokens.append(node_stack.pop())
          state_stack.pop()

        child_tokens.reverse()
        node_stack.append(TreeNode(LHS, child_tokens))
        state_stack.append(Trans(state_stack[-1], LHS))
          
        reduction = Reduce(state_stack[-1], token)

      node_stack.append(TreeNode(token))
      if Trans(state_stack[-1], token) == 'ERROR'
        raise Exception('Parsing error')
      state_stack.append(Trans(state_stack[-1], token))

    # node_stack should be [TreeNode("$"), ParseTree, TreeNode("$")]
    assert(len(node_stack) == 3)
    assert(node_stack[0].value == "$")
    assert(node_stack[2].value == "$")
    return node_stack[1]
