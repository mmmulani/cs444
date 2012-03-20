public class Je_Reachability_Inside_Block {
  public Je_Reachability_Inside_Block() { }

  public void test() {
    while (true) {
      while (false) { }
    }
  }
}
