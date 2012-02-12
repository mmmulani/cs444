import os

from tree_node import TreeNode
from scanner.scanner import TokenType

class ParsingError(Exception):
  pass

class Parser(object):
  '''Parser object
  Takes a list of tokens, and returns a parse tree if the tokens can be
  successfully parsed (otherwise, an exception is thrown)
  '''

  def __init__(self, reduce_filename = '', shift_filename = ''):
    if reduce_filename == '':
      reduce_filename = os.path.join(
          os.path.dirname(__file__), '../utils/joos_reduce.txt')
      if shift_filename == '':
        shift_filename = os.path.join(
            os.path.dirname(__file__), '../utils/joos_shift.txt')

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
    for i in xrange(len(tokens)):
      token = tokens[i]
      token_type, lexeme = token.type, token.lexeme
      reduction = Reduce.get((state_stack[-1], token_type), None)
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
        node_stack.append(TreeNode(LHS, '', child_tokens))
        state_stack.append(Shift[(state_stack[-1], LHS)])

        reduction = Reduce.get((state_stack[-1], token_type), None)

      # we couldn't reduce, so try a shift:
      node_stack.append(TreeNode(token_type, lexeme))
      shift = Shift.get((state_stack[-1], token_type), None)
      if shift == None:
        # self._debug_output(tokens, i, node_stack)
        raise ParsingError('No shift rule found: error parsing tokens!')
      state_stack.append(shift)

    # node_stack should be [BOF, StartSymbol, EOF]
    if (len(node_stack) != 3 or node_stack[0].value != TokenType.BOF or
        node_stack[2].value != TokenType.EOF):
      raise ParsingError('Node stack incorrect after processing token list')
    return node_stack[1]

  def _debug_output(self, tokens, i, node_stack):
    print "Tokens processed:"
    print tokens[:i]
    print "\nTokens remaining:"
    print tokens[i:]
    print "\nTree stack:"
    for tree in node_stack:
      tree.pretty_print()
      print "------"
