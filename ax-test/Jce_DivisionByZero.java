public class Jce_DivisionByZero {
  public Jce_DivisionByZero() {}

  public static int func() {
    return 49;
  }

  public static int test() {
    int x = 49;
    int y = 1 / (x - Jce_DivisionByZero.func());
    return 123;
  }
}
