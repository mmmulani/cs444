public class Jce_ArrayOutOfBoundsNegative {
  public Jce_ArrayOutOfBoundsNegative() {}

  public static int test() {
    int[] a = new int[57];
    a[-5] = 666;
    return 123;
  }
}
