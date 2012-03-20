public class Je_ConstantFoldingOverflow {
  Je_ConstantFoldingOverflow() { }

  public void method() {
    // Constant folding should detect that the while expression equals false
    // (because of overflow) which should cause a reachability error
    while  ((2147483647 + 1 > 0) || (-2147483648 - 1 < 0)) {}

  }


}
