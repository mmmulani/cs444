public class Board {
  public int[] dots;
  public int width;
  public Board(int width) {
    dots = new int[width * width];
    this.width = width;
  }

  public Board advance() {
    Board ret = new Board(width);

    for (int i = 0; i < width; i = i + 1) {
      for (int j = 0; j < width; j = j + 1) {
        int dots = this.aliveNeighbours(i, j);

        boolean alive = false;
        if (getSpot(i, j) == 0) {
          alive = dots == 3;
        } else {
          alive = dots > 1 && 3 >= dots;
        }
        int value = 0;
        if (alive) {
          value = 1;
        } else {
        }

        ret.setSpot(i, j, value);
      }
    }

    return ret;
  }

  public int aliveNeighbours(int i, int j) {
    int x_min = i - 1;
    if (x_min < 0)
      x_min = 0;

    int x_max = i + 1;
    if (x_max >= width)
      x_max = width - 1;

    int y_min = j - 1;
    if (y_min < 0)
      y_min = 0;

    int y_max = j + 1;
    if (y_max >= width)
      y_max = width - 1;

    int total_dots = 0;

    for (int x = x_min; x <= x_max; x = x + 1) {
      for (int y = y_min; y <= y_max; y = y + 1) {
        if (x != i || y != j) {
          total_dots = total_dots + getSpot(x, y);
        }
      }
    }

    return total_dots;
  }

  public void setSpot(int x, int y, int val) {
    dots[y * width + x] = val;
  }

  public int getSpot(int x, int y) {
    return dots[y * width + x];
  }
}
