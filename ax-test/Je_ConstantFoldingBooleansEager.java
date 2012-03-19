public class Je_ConstantFoldingBooleansEager {
  Je_ConstantFoldingBooleansEager() { }

  public void method() {

    // Constant folding should detect that the while expression equals false,
    // which should cause a reachability error
    while (false & (true | false)) {}

  }


}
