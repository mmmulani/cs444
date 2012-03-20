/* Tests that supertypes are not assignable to their subtypes.*/
public class Bar extends Foo {
  Bar() {}

  public void bar() {
    Foo f = new Foo();
    Bar b = new Bar();
    b = f;
  }
}
