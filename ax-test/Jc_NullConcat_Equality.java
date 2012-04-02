public class Jc_NullConcat_Equality {
  public Jc_NullConcat_Equality() { }

  public static int test() {
    String s = "1" + null;
    if (s.equals((Object) "1null")) {
      return 123;
    } else {
      return 1;
    }
  }
}

