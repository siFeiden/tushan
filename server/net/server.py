import asyncio as aio
import json
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
  def __init__(self, id, json):
    super().__init__()
    self.id = id
    self.json = json


class InvalidMessageReceivedEvent(Event):
  def __init__(self, id, payload, exception):
    super().__init__()
    self.id = id
    self.payload = payload
    self.exception = exception


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
    self.event_queue.register_class(SpawnReadersListener())
    self.event_queue.register_class(Broadcaster())

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
      payload = line.decode('utf-8')

      try:
        content = json.loads(payload)
        event = MessageReceivedEvent(self.id, content)
      except json.JSONDecodeError as e:
        if self.reader.at_eof():
          break # drop last partial message

        event = InvalidMessageReceivedEvent(self.id, payload, e)

      await self.event_queue.publish(event)

      if self.reader.at_eof():
        break

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
        payload = json.dumps(event.json)
        client.write(payload.encode('utf-8'))
        await client.drain()
    elif isinstance(event, ClientDisconnectedEvent):
      self.clients.pop(event.id)
