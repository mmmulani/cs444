public class J1_ConstantFoldingMethodInvocation {
  public J1_ConstantFoldingMethodInvocation() {
    while (false & J1_ConstantFoldingMethodInvocation.foo()) {
      // This will never be reached and the compiler could know because of
      // eager boolean operations BUT, by the spec, it should not consider
      // it to be a constant expression.
    }
  }

  public static boolean foo() {
    return false;
  }
}
