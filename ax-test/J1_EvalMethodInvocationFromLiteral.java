public class J1_EvalMethodInvocationFromLiteral {
  public J1_EvalMethodInvocationFromLiteral() {
    // Method invocation can occur on a non-parenthesized expression.
    String b = "abc".toString();
    b = (b = "123".toString()) + null + 123;
  }
}
