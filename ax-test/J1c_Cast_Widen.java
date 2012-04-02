public class J1c_Cast_Widen {
  public J1c_Cast_Widen() {
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Test.test());
  }

  public static int test() {
    int a = 255 * 256 + 255; // 0xffff
    int b = 255 * a + 255; // 0xffffff
    int c = ((int) (byte) a); // 0xffffffff by sign extend
    if (c == -1) {
      return 123;
    } else {
      return 18;
    }
  }
}
