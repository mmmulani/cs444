/* Duplicate methods with the same type (but different type name) should not
 * compile. */
public class Je_x_DuplicateMethodDifferentType {
  public Je_x_DuplicateMethodDifferentType() {}

  public java.lang.String test() { }

  public String test() { }
}
