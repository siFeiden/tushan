import unittest

from arena.logic.game import Board, Game, Player
from arena.logic.piece import DockingPoint, Orientation, Piece, PlacedPiece


class GameScoreTest(unittest.TestCase):
  def setUp(self):
    self.pieces = [
        Piece(2, 2, [0, 1, 2, 3, 4, 5, 6, 7]),
        Piece(1, 3, [0, 4, 7]),
        Piece(1, 3, [0, 4]),
        Piece(3, 2, [3, 6, 8, 9]),
        Piece(1, 3, [0, 4]),
        Piece(1, 3, [0, 4]),
        Piece(3, 1, [1, 3, 7])
    ]

    self.player1 = Player(1)
    self.player2 = Player(2)
    self.players = [self.player1, self.player2]
    self.objectives = {
      self.player1: [Board.Side.East, Board.Side.West],
      self.player2: [Board.Side.North, Board.Side.South]
    }

  def test_score_no_connectors_on_edges(self):
    board = Board(10)
    game = Game(board, self.players, self.objectives, self.pieces)

    expected_scores = {p: 0 for p in self.players}
    self.assertDictEqual(expected_scores, game.scores())

  def test_trivial_board(self):
    board = Board(2)
    game = Game(board, self.players, self.objectives, self.pieces)
    game.make_turn(self.player1, self.pieces[0], 0, 0, Orientation.South)

    expected_scores = {p: 4 for p in self.players}
    self.assertDictEqual(expected_scores, game.scores())

  def test_large_board(self):
    """Test score of the following board:
      0  1  2  3  4  5  6  7  8
    0 +--+oo+--+oo+oo+  +  +  +
      o   p7   |  |  |
    1 +--+--+--+  +  +  .  .  +
               |p2|p3|
    2 +  .  .  +  +  +  .  .  +
               |  |  |
    3 +  .  .  +oo+oo+--+--+--+
               o     o        |
    4 +  .  .  + p1  +   p4   +
               o     o        o
    5 +  .  .  +oo+oo+--+oo+--+
                  |  |  |  |
    6 +  .  .  .  +  +  +  +  +
                  |p6|  |p5|
    7 +  .  .  .  +  +  +  +  +
                  |  |  |  |
    8 +  +  +  +  +oo+  +oo+  +
    """
    p1, p2, p3, p4, p5, p6, p7 = self.pieces

    board = Board(8)
    game = Game(board, self.players, self.objectives, self.pieces)
    game.make_turn(self.player1, p1, 3, 3, Orientation.South)
    game.make_turn(self.player2, p2, 3, 0, Orientation.South)
    game.make_turn(self.player1, p3, 4, 0, Orientation.South)
    game.make_turn(self.player2, p4, 5, 3, Orientation.South)
    game.make_turn(self.player1, p5, 6, 5, Orientation.South)
    game.make_turn(self.player2, p6, 4, 5, Orientation.South)
    game.make_turn(self.player1, p7, 0, 0, Orientation.South)

    expected_scores = {
      self.player1: 1,
      self.player2: 6
    }
    self.assertDictEqual(expected_scores, game.scores())
