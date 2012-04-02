public class Jc_ArrayEquals {
  public Jc_ArrayEquals() { }

  public static int test() {
    boolean[] x = new boolean[20];
    boolean[] y = new boolean[20];

    for (int i = 0; i < x.length; i = i + 1) {
      boolean v = true;
      if (i % 2 == 0) {
        v = false;
      }
      x[i] = v;
      y[i] = v;
    }

    if (java.util.Arrays.equals(x, y)) {
      return 123;
    }
    return 0;
  }
}
