public class Jce_ArrayCreateNegativeLength {
  public Jce_ArrayCreateNegativeLength() {}

  public static int neg = -1;

  public static int test() {
    int[] array = new int[Jce_ArrayCreateNegativeLength.neg];
    return 123;
  }
}
