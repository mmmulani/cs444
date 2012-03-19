public class Je_ConstantFoldingBooleans {
  Je_ConstantFoldingBooleans() { }

  public void method() {

    // Constant folding should detect that the while expression equals false,
    // which should cause a reachability error
    while (false || (true && false) || (false || false)) {}

  }


}
