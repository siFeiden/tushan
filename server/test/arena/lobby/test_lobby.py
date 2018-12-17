from asynctest import TestCase

from test.games import GamePlan, GameSpec


class LobbyTest(TestCase):
  async def test_spec_game(self):
    gamespec = GameSpec.from_file('../protocol/examples/populated-field.json')
    gameplan = GamePlan(gamespec)
    await gameplan.execute()
