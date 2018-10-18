import asyncio as aio

from collections import defaultdict
from datetime import datetime


class Event(object):
  def __init__(self):
    self.occured = datetime.now()
    self.event_queue = None


class HandlerFailedEvent(object):
  def __init__(self, handler):
    super().__init__()
    self.failed_handler = failed_handler


class EventQueue(object):
  def __init__(self):
    self.queue = aio.Queue()
    self.handlers = defaultdict(list)
    self.any_handlers = []

  def register(self, event_class, handler):
    self.handlers[event_class].append(handler)

  def register_for_all(self, handler):
    self.any_handlers.append(handler)

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
      for handler in self.handlers[event_class]:
        await self.fire_event(event, handler)

      for handler in self.any_handlers:
        await self.fire_event(event, handler)

      self.queue.task_done()

  async def fire_event(self, event, handler):
      event_class = type(event)
      try:
        result = handler(event)

        # event handler may be async
        if aio.iscoroutine(result):
          await result
      except:
        await self.publish(HandlerFailedEvent(handler))
