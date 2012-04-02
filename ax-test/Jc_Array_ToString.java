public class Jc_Array_ToString {
  public Jc_Array_ToString() { }

  public static int test() {
    int[] x = new int[20];
    if ("Some random object".equals((Object) ((Object) x).toString())) {
      return 123;
    }
    return 123;
  }
}
