import json
import unittest

from arena.logic.piece import Orientation, Piece, PlacedPiece
from arena.logic.game import Board, Game, Player
from arena.serializers import *


class SerializerSpecTest(unittest.TestCase):
  def assertSerializationEqual(self, spec_file, actual):
    with open(spec_file) as f:
      spec = json.load(f)
      self.assertDictEqual(spec, actual)

  def test_piece_spec(self):
    piece = Piece(3, 1, [0, 3, 7])
    serialized = PieceSerializer.serialize(piece)
    spec_file = '../protocol/examples/not-placed-stone.json'
    self.assertSerializationEqual(spec_file, serialized)

  def test_placed_piece_spec(self):
    player = Player(1)
    player.name = 'abraham'

    piece = Piece(3, 1, [0, 3, 7])
    placed_piece = PlacedPiece(piece, 1, 3, Orientation.South, player)

    serialized = PlacedPieceSerializer.serialize(placed_piece)
    spec_file = '../protocol/examples/placed-stone.json'
    self.assertSerializationEqual(spec_file, serialized)

  def game_spec_pieces(self):
    return [
      Piece(2, 2, [3, 4, 5, 7]),
      Piece(4, 1, [2, 6, 8]),
      Piece(3, 1, [1, 2, 7]),
      Piece(3, 2, [0, 4, 9]),
      Piece(2, 1, [0, 3, 4])
    ], [
      (5, 4, Orientation.South),
      (4, 5, Orientation.East),
      (5, 2, Orientation.South),
      (1, 1, Orientation.South),
      (2, 1, Orientation.North)
    ]


  def test_game_spec(self):
    player1 = Player('Player A')
    player1.name = player1.id

    player2 = Player('Player B')
    player2.name = player2.id

    objectives = {
      player1: [Board.Side.North, Board.Side.South],
      player2: [Board.Side.East, Board.Side.West]
    }

    pieces, positions = self.game_spec_pieces()

    board = Board(10)
    game = Game(board, [player1, player2], objectives, pieces)

    for piece, pos in zip(pieces, positions):
      game.make_turn(game.current_player, piece, *pos)

    serialized = GameSerializer.serialize(game)
    spec_file = '../protocol/examples/populated-field.json'
    self.assertSerializationEqual(spec_file, serialized)
