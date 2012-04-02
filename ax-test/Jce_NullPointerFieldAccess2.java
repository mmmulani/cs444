public class Jce_NullPointerFieldAccess2 {
  public Jce_NullPointerFieldAccess2 a;
  public int b;

  public Jce_NullPointerFieldAccess2() {
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Jce_NullPointerFieldAccess2.test());
  }

  public static int test() {
    // Should have a null pointer exception.
    ((Jce_NullPointerFieldAccess2) null).a = new Jce_NullPointerFieldAccess2();

    return 18;
  }
}
