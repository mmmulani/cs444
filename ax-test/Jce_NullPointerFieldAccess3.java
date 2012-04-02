public class Jce_NullPointerFieldAccess3 {
  public Jce_NullPointerFieldAccess3 a;
  public int b;

  public Jce_NullPointerFieldAccess3() {
    // Should have a null pointer exception.
    a.a = new Jce_NullPointerFieldAccess3();
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Jce_NullPointerFieldAccess3.test());
  }

  public static int test() {
    new Jce_NullPointerFieldAccess3();

    return 18;
  }
}
