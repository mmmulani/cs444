public class Jce_NullPointerArrayWrite {
  public Jce_NullPointerArrayWrite() {
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Jce_NullPointerArrayWrite.test());
  }

  public static int test() {
    int[] b = null;
    // Should have a null pointer exception.
    b[0] = 1;

    return 18;
  }
}
