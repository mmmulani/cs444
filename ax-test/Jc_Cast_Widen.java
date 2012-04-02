public class Jc_Cast_Widen {
  public Jc_Cast_Widen() {
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Jc_Cast_Widen.test());
  }

  public static int test() {
    int a = 255 * 256 + 255; // 0xffff
    int b = 255 * a + 255; // 0xffffff
    int c = ((int) (byte) a); // 0xffffffff by sign extend
    int d = (int) (short) a; // also 0xffffff by sign extend
    if (c != -1) {
      return 18;
    }
    if (d != -1) {
      return 18;
    }

    return 123;
  }
}
