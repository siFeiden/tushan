from net.server import *
from test.event_queue import EventQueueTestMixin
from asynctest import CoroutineMock, MagicMock, TestCase


class ReaderTest(TestCase, EventQueueTestMixin):
  async def test_valid_json(self):
    id = 'abcde'
    event_queue = self.event_queue_mock()

    streamreader = MagicMock()
    streamreader.readline = CoroutineMock(return_value=b'{}')
    streamreader.at_eof = MagicMock(return_value=True)

    reader = Reader(id, event_queue, streamreader)
    await reader.run()

    expected_events = [MessageReceivedEvent, ClientDisconnectedEvent]
    self.assertEventSequence(event_queue, expected_events)

  async def test_invalid_json(self):
    id = 'abcde'
    event_queue = self.event_queue_mock()

    streamreader = MagicMock()
    streamreader.readline = CoroutineMock(return_value=b'{"invalid"')
    streamreader.at_eof = MagicMock(side_effect=[False, True])

    reader = Reader(id, event_queue, streamreader)
    await reader.run()

    expected_events = [InvalidMessageReceivedEvent, ClientDisconnectedEvent]
    self.assertEventSequence(event_queue, expected_events)
