public class Je_Reachability_Ifs_No_Returns {
  public Je_Reachability_Ifs_No_Returns() { }
  public int test() {
    if (true) {
      int x = 3;
      if (x == 4) {
        int y = 1;
        if (y == 1) {
          return 42;
        } else {
          return 42;
        }
      } else {
        return 1;
      }
    }
  }
}
