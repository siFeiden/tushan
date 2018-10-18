import asyncio as aio
import uuid

from eventing.event_queue import Event


class ClientConnectedEvent(Event):
  def __init__(self, id, reader, writer):
    super().__init__()
    self.id = id
    self.reader = reader
    self.writer = writer


class ClientDisconnectedEvent(Event):
  def __init__(self, id):
    super().__init__()
    self.id = id


class MessageReceivedEvent(Event):
  def __init__(self, id, payload):
    super().__init__()
    self.id = id
    self.payload = payload


class Server(object):
  def __init__(self, event_queue, host, port):
    self.event_queue = event_queue
    self.host = host
    self.port = port

  async def client_connected(self, reader, writer):
    client_id = uuid.uuid4()
    event = ClientConnectedEvent(client_id, reader, writer)
    await self.event_queue.publish(event)

  async def start(self):
    await aio.start_server(
      self.client_connected,
      self.host,
      self.port
    )


class Reader(object):
  def __init__(self, id, event_queue, reader):
    self.id = id
    self.event_queue = event_queue
    self.reader = reader

  async def run(self):
    while True:
      line = await self.reader.readline()
      if self.reader.at_eof():
        break # drops last partial message

      event = MessageReceivedEvent(self.id, line.decode('utf-8'))
      await self.event_queue.publish(event)

    event = ClientDisconnectedEvent(self.id)
    await self.event_queue.publish(event)


class SpawnReadersListener(object):
  events = ClientConnectedEvent

  def __call__(self, event):
    reader = Reader(event.id, event.event_queue, event.reader)
    aio.create_task(reader.run())


class Broadcaster(object):
  events = [
    ClientConnectedEvent,
    MessageReceivedEvent,
    ClientDisconnectedEvent
  ]

  def __init__(self):
    self.clients = {}

  async def __call__(self, event):
    if isinstance(event, ClientConnectedEvent):
      self.clients[event.id] = event.writer
    elif isinstance(event, MessageReceivedEvent):
      for client in self.clients.values():
        client.write(event.payload.encode('utf-8'))
        await client.drain()
    elif isinstance(event, ClientDisconnectedEvent):
      self.clients.pop(event.id)
