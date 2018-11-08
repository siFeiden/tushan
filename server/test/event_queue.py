from asynctest.mock import CoroutineMock, MagicMock
from eventing.event_queue import EventQueue


class EventQueueTestMixin(object):
  def event_queue_mock(self):
    return CoroutineMock(spec=EventQueue)

  def assertEventSequence(self, event_queue, events):
    publish_calls = event_queue.publish.call_args_list

    call_count = event_queue.publish.call_count
    if len(events) != call_count:
      raise AssertionError(f'Expected {len(events)} events, got {call_count}')

    for (args, kwargs), event in zip(publish_calls, events):
      if not isinstance(args[0], event):
        arg_type_name = type(args[0]).__name__
        raise AssertionError(f'{arg_type_name} is not a {event.__name__} event')
