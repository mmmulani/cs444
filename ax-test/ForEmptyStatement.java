public class ForEmptyStatement {
  public ForEmptyStatement() { }
  public void test() {
    for (int i = 0; i < 10; i = i + 1);
  }
}
