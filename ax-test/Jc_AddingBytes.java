public class Jc_AddingBytes {
  public Jc_AddingBytes() {}

  public static int test() {
    byte x = (byte)255;
    byte y = (byte)66;
    byte z = (byte)(x + y);
    return z + 58;
  }
}
