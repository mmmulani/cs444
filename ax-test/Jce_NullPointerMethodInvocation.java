public class Jce_NullPointerMethodInvocation {
  public Jce_NullPointerMethodInvocation() {}

  public void func() {
    System.out.println("foo!");
  }

  public int x = 99;

  public static int test() {
    Jce_NullPointerMethodInvocation f = new Jce_NullPointerMethodInvocation();
    f = null;
    f.func();
    return 123;
  }
}
