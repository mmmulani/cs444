/**
 * Usually multiple declarations of the same name in the local scope are bad but
 * Java compiles this fine. (Presumably because the declaration is made after
 * block ends.)
 */
public class J1_x_DeclarationOrder {
  public J1_x_DeclarationOrder() {}
  public static void main(String[] args) {
    {
      int y = 0;
    }
    int y = 2;
  }
}
