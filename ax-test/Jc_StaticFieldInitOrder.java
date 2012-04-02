public class Jc_StaticFieldInitOrder {
  public Jc_StaticFieldInitOrder() {}

  public static int x = Jc_StaticFieldInitOrder.y + 123; // should equal 123
  public static int y = 69;

  public static int test() {
    return Jc_StaticFieldInitOrder.x;
  }
}
