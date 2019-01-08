from collections import defaultdict
from math import ceil, floor

class AsciiBoard(object):
  priorities = {
    '*': 20,
    '+': 10,
    'o': 15,
    '-': 10,
    '|': 10,
    ' ': 0,
  }

  def __init__(self, board):
    self.board = board
    self.canvas = defaultdict(lambda: ' ')
    self.width = board.size * 3 + 1
    self.height = board.size * 2 + 1

  def paint(self):
    for piece in self.board.pieces:
      self.paint_piece(piece)

  def print(self):
    print()
    for y in range(self.height):
      for x in range(self.width):
        print(self.canvas[(x, y)], end='')
      print()

  def paint_piece(self, piece):
    self.put(3*piece.x, 2*piece.y, '*')

    for dock in piece.docking_points():
      self.paint_docking_point(dock)

    area = piece.area()
    self.paint_area_grid(area)

  def paint_area_grid(self, area):
    width = area.right - area.left
    height = area.bottom - area.top

    for dx in range(width+1):
      x = area.left + dx
      self.draw_grid_point(x, area.top)
      self.draw_grid_point(x, area.bottom)

    # skip the points drawn in loop above
    for dy in range(height-1):
      y = area.top + dy + 1
      self.draw_grid_point(area.left, y)
      self.draw_grid_point(area.right, y)

  def draw_grid_point(self, x, y):
      self.put(3 * x, 2 * y, '+')

  def paint_docking_point(self, dock):
    x = 3 * dock.x
    y = 2 * dock.y

    if dock.x.is_integer():
      c = 'o' if dock.is_connector else '|'
      self.put(x, y, c)
    else:
      assert dock.y.is_integer()

      x1, x2 = floor(x), ceil(x)
      c = 'o-' if dock.is_connector else '--'
      self.put(x1, y, c[0])
      self.put(x2, y, c[1])

  def put(self, x, y, c):
    x = int(x)
    y = int(y)
    p = self.canvas[(x, y)]
    if self.priorities[p] < self.priorities[c]:
      self.canvas[(x, y)] = c
