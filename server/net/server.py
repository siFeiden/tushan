import asyncio as aio

from eventing.event_queue import Event


class ClientConnectedEvent(Event):
  def __init__(self, reader, writer):
    super().__init__()
    self.reader = reader
    self.writer = writer


class ClientDisconnectedEvent(Event):
  pass


class MessageReceivedEvent(Event):
  def __init__(self, payload):
    super().__init__()
    self.payload = payload


class Server(object):
  def __init__(self, event_queue, host, port):
    self.event_queue = event_queue
    self.host = host
    self.port = port

  async def client_connected(self, reader, writer):
    event = ClientConnectedEvent(reader, writer)
    await self.event_queue.publish(event)

  async def start(self):
    await aio.start_server(
      self.client_connected,
      self.host,
      self.port
    )


class Reader(object):
  def __init__(self, event_queue, reader):
    self.event_queue = event_queue
    self.reader = reader

  async def run(self):
    while True:
      line = await self.reader.readline()
      if self.reader.at_eof():
        break # drops last partial message

      event = MessageReceivedEvent(line.decode('utf-8'))
      await self.event_queue.publish(event)

    event = ClientDisconnectedEvent()
    await self.event_queue.publish(event)


class SpawnReadersListener(object):
  events = ClientConnectedEvent

  def __call__(self, event):
    reader = Reader(event.event_queue, event.reader)
    aio.create_task(reader.run())
