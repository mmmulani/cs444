public class Je_ConstantFoldingOverflowUnary {
  Je_ConstantFoldingOverflowUnary() { }

  public void method() {
    // Constant folding should detect that the while expression equals false
    // (because of overflow) which should cause a reachability error
    while  (-(-2147483648) != -2147483648) {}

  }


}
