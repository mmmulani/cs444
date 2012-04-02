public class foo extends bar{
  foo() {}
  public static int test() {
    foo[] foo_array = new foo[10];
    bar b = new bar();
    foo f = new foo();
    bar[] bar_array = foo_array;
    bar_array[0] = b;   // this should throw a runtime exception
    return 123;
  }
}
