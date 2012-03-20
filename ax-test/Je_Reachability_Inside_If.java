public class Je_Reachability_Inside_If {
  public Je_Reachability_Inside_If() { }

  public void test() {
    if (false) {
      // We still should be checking in here.
      while (false) { } // Should be an error.
    }
  }
}
