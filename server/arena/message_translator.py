from .logic.piece import Orientation
from .events import *
from net.server import MessageReceivedEvent


class MessageTranslator(object):
  """Translates MessageReceivedEvents into more specific events"""

  def __call__(self, event):
    """This method receives the bootstrap event"""
    event.event_queue.register(MessageReceivedEvent, self.onMessageReceived)

  async def onMessageReceived(self, event):
    player_id = event.id
    content = event.json

    translation = self.translate(content, player_id)
    await event.event_queue.publish(translation)

  def translate(self, content, player_id):
    message_type = content['type']

    if message_type == 'name':
      name = content['name']
      return PlayerNameEvent(player_id, name)
    elif message_type == 'move':
      x = content['x']
      y = content['y']
      orientation = Orientation(content['orientation'])
      return PlayerMoveEvent(player_id, x, y, orientation)
    elif message_type == 'gameover':
      return PlayerCannotMoveEvent(player_id)

    return BadMessageReceivedEvent(player_id, content)
