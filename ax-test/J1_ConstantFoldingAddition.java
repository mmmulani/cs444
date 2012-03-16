public class J1_ConstantFoldingAddition {
  public J1_ConstantFoldingAddition() {}

  public int test() {
    // Should pass since (1 + 1 == 2) => true, so
    // OUT of the while statement is NO
    while (1 + 1 == 2) { }
  }
}
