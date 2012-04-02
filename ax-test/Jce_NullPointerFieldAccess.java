public class Jce_NullPointerFieldAccess {
  public Jce_NullPointerFieldAccess() {}

  public void func() {
    System.out.println("foo!");
  }

  public int x = 99;

  public static int test() {
    Jce_NullPointerFieldAccess f = new Jce_NullPointerFieldAccess();
    f = null;
    System.out.println(f.x);
    return 123;
  }
}
