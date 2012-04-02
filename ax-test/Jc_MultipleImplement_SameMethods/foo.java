public class foo implements bar, baz {
  public foo() { }

  public int m() {
    return 123;
  }

  public int m2() {
    return 12;
  }

  public static int test() {
    foo f = new foo();
    int s = f.m2();
    return f.m();
  }
}
