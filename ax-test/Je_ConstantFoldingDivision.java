public class Je_ConstantFoldingDivision {
  Je_ConstantFoldingDivision() { }

  public void method() {

    // Constant folding should detect that the while expression equals false,
    // (because integer division rounds down), which should cause a
    // reachability error
    while (5 / 2 > 2) {}

  }


}
