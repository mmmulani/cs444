public class Je_ConstantFoldingMath {
  Je_ConstantFoldingMath() { }

  public void method() {

    // Constant folding should detect that the while expression equals false,
    // which should cause a reachability error
    while ((1+2) == 5 || (7+9) > (100+5)) {}

  }


}
