/* Tests that subtypes are assignable to their supertypes.*/
public class Bar extends Foo {
  Bar() {}

  public void bar() {
    Foo f = new Foo();
    Bar b = new Bar();
    f = b;

    Foo [] f_array = new Foo[10];
    Bar [] b_array = new Bar[10];
    f_array = b_array;
  }
}
