public class J1_ConstantFoldingStringPlus {
  J1_ConstantFoldingStringPlus() { }

  public void method() {

    // Constant folding should detect that the while expression equals true,
    // which should NOT cause a reachability error
    while ("abc123" == "a" + "b" + "c" + 1 + 2 + 3 ) {}

  }


}
