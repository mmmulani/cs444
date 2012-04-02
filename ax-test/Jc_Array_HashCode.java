public class Jc_Array_HashCode {
  public Jc_Array_HashCode() { }

  public static int test() {
    boolean[] x = new boolean[20];
    boolean[] y = new boolean[20];

    return ((Object) x).hashCode() + ((Object) y).hashCode() + ((Object) y).hashCode() - 3;

  }
}
