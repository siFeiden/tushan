from .logic.piece import Orientation


class MessageTranslator(object):
  """Translates MessageReceivedEvents into more specific events"""

  def __init__(self, event_queue):
    self.event_queue = event_queue

  # TODO: register method in event_queue
  async def onMessageReceived(self, event):
    player_id = event.id
    content = event.content

    translation = self.translate(content, event.id)
    await self.event_queue.publish(translation)

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
      return PlayerGameOverEvent(player_id)

    return BadEventReceivedEvent(player_id, content)
