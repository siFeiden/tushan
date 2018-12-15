class Serializer(object):
  @classmethod
  def serialize_many(clss, objects):
    assert(objects is not None)

    return [clss.serialize(o) for o in objects]


class EnumSerializer(Serializer):
  @staticmethod
  def serialize(enum_option):
    assert(enum_option is not None)

    return enum_option.value


class PieceSerializer(Serializer):
  @staticmethod
  def serialize(piece):
    assert(piece is not None)

    return {
      'width': piece.width,
      'height': piece.height,
      'connectors': list(piece.connectors)
    }


class PlacedPieceSerializer(Serializer):
  @staticmethod
  def serialize(piece):
    assert(piece is not None)

    serialpiece = PieceSerializer.serialize(piece.piece)
    return {
      'x': piece.x,
      'y': piece.y,
      'orientation': piece.orientation.value,
      'player': PlayerSerializer.serialize(piece.player),
      **serialpiece
    }


class PlayerSerializer(Serializer):
  @staticmethod
  def serialize(player):
    return {
      'id': str(player.id),
      'objectives': [o.value for o in player.objectives]
    }


class BoardSerializer(Serializer):
  @staticmethod
  def serialize(board):
    assert(board is not None)

    return {
      'size': board.size,
      'pieces': PlacedPieceSerializer.serialize_many(board.pieces)
    }


class GameSerializer(Serializer):
  @staticmethod
  def serialize(game):
    assert(game is not None)

    return {
      'board': BoardSerializer.serialize(game.board),
      'players': PlayerSerializer.serialize_many(game.players)
    }
