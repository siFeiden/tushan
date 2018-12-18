from asynctest import TestCase

from arena.events import GameIsOverEvent, MoveAcceptedEvent
from test.event_queue import EventQueueTestMixin
from test.games import GamePlan, GameSpec


class LobbyTest(TestCase, EventQueueTestMixin):
  async def test_spec_game(self):
    gamespec = GameSpec.from_file('../protocol/examples/populated-field.json')
    gameplan = GamePlan(gamespec)
    event_queue = self.event_queue_mock()
    await gameplan.execute_on(event_queue)

    moves = len(gamespec.pieces) - 1
    # last successful moves generates GameIsOverEvent
    events = [*[MoveAcceptedEvent] * moves, GameIsOverEvent]
    self.assertEventsFuzzy(event_queue, events)
