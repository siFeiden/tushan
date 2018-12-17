import asyncio as aio
import traceback

from collections import defaultdict
from datetime import datetime


class Event(object):
  def __init__(self):
    self.occured = datetime.now()
    self.event_queue = None


class HandlerFailedEvent(Event):
  def __init__(self, failed_handler, exception):
    super().__init__()
    self.failed_handler = failed_handler
    self.exception = exception


class EventQueue(object):
  def __init__(self, debug=False):
    self.debug = debug
    self.queue = aio.Queue()
    self.handlers = defaultdict(list)

  def register(self, event_class, handler):
    self.handlers[event_class].append(handler)

  def register_class(self, clss):
    try:
      # can also be a list of events
      for event_class in clss.events:
        self.register(event_class, clss)
    except TypeError:
      self.register(clss.events, clss)

  async def publish(self, event):
    await self.queue.put(event)

  async def run(self):
    while True:
      event = await self.queue.get()
      event.event_queue = self

      event_class = type(event)
      if self.debug:
        print('Handle', event_class.__name__)

      for handler in self.handlers[event_class]:
        await self.fire_event(event, handler)

      self.queue.task_done()

  async def fire_event(self, event, handler):
      event_class = type(event)
      try:
        result = handler(event)

        # event handler may be async
        if aio.iscoroutine(result):
          await result
      except Exception as e:
        if self.debug:
          traceback.print_exc()
        await self.publish(HandlerFailedEvent(handler, e))
