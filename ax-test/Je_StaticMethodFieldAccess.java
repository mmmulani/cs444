public class Je_StaticMethodFieldAccess {
  public Je_StaticMethodFieldAccess() { }

  public int board_size = 2;
  public static int test() {
    // Can not access board_size (it's an instance field).
    int c = board_size;
  }
}
