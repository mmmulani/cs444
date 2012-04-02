public class Jc_GameOfLife {
  public Jc_GameOfLife() {
  }

  public static void main(String[] args) {
    System.out.println("Return code: " + Jc_GameOfLife.test());
  }

  public static int board_size = 10;
  public static int test() {
    Board game_board = new Board(Jc_GameOfLife.board_size);

    String[] board_str = new String[5];
    //              --------
    board_str[0] = "        ";
    board_str[1] = "    X X ";
    board_str[2] = "    X X ";
    board_str[3] = "    XXX ";
    board_str[4] = "        ";
    //              --------

    // Init the board.
    int i = 0;
    while (i < board_str.length) {
      for (int j = 0; j < board_str[i].length(); j = j + 1) {
        if (board_str[i].charAt(j) == 'X') {
          game_board.setSpot(j, i, 1);
        }
      }
      i = i + 1;
    }

    int num_turns = 46;
    for (int k = 0; k < num_turns; k = k + 1) {
      System.out.println("Turn " + k);
      Jc_GameOfLife.drawBoard(game_board);

      game_board = game_board.advance();

      for (int j = 0; j < 200000; j = j + 1) {
      }
    }

    return 123;
  }

  public static void drawBoard(Board board) {
    int board_size = Jc_GameOfLife.board_size;
    for (int y = -1; y <= board_size; y = y + 1) {
      System.out.print('-');
    }
    System.out.print('\n');

    for (int y = 0; y < board_size; y = y + 1) {
      for (int x = 0; x < board_size; x = x + 1) {
        int val = board.getSpot(x, y);
        char to_pr = ' ';
        if (val > 0) {
          to_pr = 'O';
        } else {
          to_pr = ' ';
        }
        System.out.print(to_pr);
      }
      System.out.print('\n');
    }

    for (int y = -1; y <= board_size; y = y + 1) {
      System.out.print('-');
    }
    System.out.print('\n');
  }
}
