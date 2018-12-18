from eventing.event_queue import EventQueue


class EventQueueTestMixin(object):
  def event_queue_mock(self):
    return TestingEventQueue()

  def assertEventSequence(self, event_queue, events):
    actual_events = event_queue.all_events
    call_count = len(actual_events)
    if len(events) != call_count:
      raise AssertionError(f'Expected {len(events)} events, got {call_count}')

    for published, expected in zip(actual_events, events):
      if not isinstance(published, expected):
        arg_type = type(published).__name__
        raise AssertionError(f'{arg_type} is not a {expected.__name__} event')

  def assertEventPublishedNTimes(self, event_queue, n, event):
    i = 0
    for published in event_queue.all_events:
      if isinstance(published, event):
        i += 1

    if i != n:
      raise AssertionError(f'{event.__name__} expected {n} times but found {i} times')

  def assertEventsFuzzy(self, event_queue, events):
    events = list(events) # copy to not modify passed list
    for published in event_queue.all_events:
      if isinstance(published, events[0]):
        events.pop(0)
        if len(events) == 0:
          return # found all events

    remaining = len(events)
    if remaining > 0:
      names = ', '.join(e.__name__ for e in events)
      raise AssertionError(f'Expected to match {remaining} more events: [{names}]')


class TestingEventQueue(EventQueue):
  """Extends a normal EventQueue and keeps all
  events that are published
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.all_events = []

  async def publish(self, event):
    self.all_events.append(event)
    return await super().publish(event)
