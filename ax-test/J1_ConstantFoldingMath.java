public class J1_ConstantFoldingMath {
  J1_ConstantFoldingMath() { }

  public void method() {

    // Constant folding should detect that the while expression equals true,
    // which should NOT cause a reachability error
    while ((1+2) == 3 && (7+9) < (100+5)) {}

  }


}
