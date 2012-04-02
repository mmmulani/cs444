public class Jce_ArrayOutOfBoundsGreaterThanLength {
  public Jce_ArrayOutOfBoundsGreaterThanLength() {}

  public static int test() {
    int[] a = new int[57];
    a[58] = 666;
    return 123;
  }
}
