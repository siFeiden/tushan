import asyncio as aio
import json
import uuid

from eventing.event_queue import Event
from arena.events import *


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

  async def start(self):
    self.event_queue.register_class(Broadcaster())

    await aio.start_server(
      self.client_connected,
      self.host,
      self.port
    )

  async def client_connected(self, reader, writer):
    client_id = uuid.uuid4()
    self.spawn_reader(client_id, reader)
    event = ClientConnectedEvent(client_id, reader, writer)
    await self.event_queue.publish(event)

  def spawn_reader(self, client_id, reader):
    reader = Reader(client_id, self.event_queue, reader)
    aio.create_task(reader.run())


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


class Broadcaster(object):
  events = [
    ClientConnectedEvent,
    MessageReceivedEvent,
    ClientDisconnectedEvent,
    GameStartedEvent,
    MoveAcceptedEvent,
    GameIsOverEvent,
    GameEndedEvent,
    GameCancelledEvent,
    FirstTurnEvent
  ]

  def __init__(self):
    self.clients = {}

  async def __call__(self, event):
    if isinstance(event, ClientConnectedEvent):
      self.clients[event.id] = event.writer
    elif isinstance(event, ClientDisconnectedEvent):
      self.clients.pop(event.id)
    else:
      try:
        data = event.to_json()
        payload = json.dumps(data) + '\n'
        for client in self.clients.values():
          client.write(payload.encode('utf-8'))
          await client.drain()
      except AttributeError as e:
        # event cannot be serialized, so don't send it
        pass

