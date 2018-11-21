from .piece import Orientation, Piece, PlacedPiece


class ValidPlacements(object):
  def __init__(self, board, piece):
    self.board = board
    self.piece = piece

  def __iter__(self):
    size = self.board.size + 1
    for x in range(size):
      for y in range(size):
        for o in Orientation:
          placed_piece = PlacedPiece(self.piece, x, y, o, None)
          try:
            self.board.validate_placement(placed_piece)
            yield placed_piece
          except:
            continue
