public class Jc_StringObjectEquality_Folding {
  public Jc_StringObjectEquality_Folding() { }

  public static void main(String[] args) {
    if ("x" == "x") {
      System.out.println("Java goes here.");
    } else {
      System.out.println("Java does not go here.");
    }
  }
  
  public static int test() {
    if ("x" == "x") {
      return 123;
    }
    return 123;
  }
}
