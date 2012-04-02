public class Jc_RecursiveFunction {
  Jc_RecursiveFunction() {}
  public static int add(int x, int y) {
    if (y == 0) {
      return x;
    }
    return Jc_RecursiveFunction.add(x+1, y-1);
  }

  public static int test() {
    int a = 23;
    int b = 100;
    int z = Jc_RecursiveFunction.add(a, b);
    return z;
  }
}
