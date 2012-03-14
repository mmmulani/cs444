public class J1_LocalSelfInitAssign {
  public J1_LocalSelfInitAssign() { }
  public void test() {
    int x = 1 + (x = 4); // Should pass as we are assigning.
  }
}
