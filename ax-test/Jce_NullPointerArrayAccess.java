public class Jce_NullPointerArrayAccess {
  public Jce_NullPointerArrayAccess a;
  public int b;

  public Jce_NullPointerArrayAccess() {
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Jce_NullPointerArrayAccess.test());
  }

  public static int test() {
    int[] b = null;
    // Should have a null pointer exception.
    int c = b[0];

    return 18;
  }
}
