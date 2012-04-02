public class Jc_BubbleSort {
  public Jc_BubbleSort() { }

  public static int test() {
    boolean swapped = true;
    int[] a = new int[200];
    for (int i = 0; i < a.length; i = i + 1) {
      a[i] = 200 - i - 1;
    }

    while (swapped) {
      swapped = false;
      for (int i = 1; i < a.length; i = i + 1) {
        if (a[i-1] > a[i]) {
          int temp = a[i-1];
          a[i-1] = a[i];
          a[i] = temp;
          swapped = true;
        }
      }
    }

    // Check the array is in sorted order.
    for (int i = 0; i < a.length; i = i + 1) {
      if (a[i] != i) {
        return 0;
      }
    }

    return 123;
  }
}
