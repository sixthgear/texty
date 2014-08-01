from texty.engine.character import Character
from texty.builtins.characters import body
from texty.util.enums import EQ_PARTS, CHAR_STATE, CHAR_FLAG
from texty.util import objectlist
from collections import OrderedDict



class Player(Character):

    attributes = 'player'

    # hacky object list to allow noun resolution for body parts
    # this gives players an objectlist to target.
    body = objectlist((
        body.Body(),
        body.Legs(),
        body.Feet(),
        body.Head(),
        body.Arms(),
        body.Neck(),
        body.Waist(),
        body.Shoulders(),
        body.FingerLeft(),
        body.FingerRight(),
        body.HandLeft(),
        body.HandRight(),
    ))

    def __init__(self, name, node=None, connection=None):

        super(self.__class__, self).__init__(name, node)
        # players are associated with a server connection
        self.connection = connection
        self.occupation = 'Former Computer Programmer'

        # take a copy, since we modify this directly and don't want to change nouns
        # for everyone of class Player!
        self.nouns = self.__class__.nouns.copy()

    def on_connect(self):
        pass

    def on_reconnect(self):
        pass

    def on_disconnect(self):
        pass

    def send(self, message):
        """
        Write a message to this player
        """
        if self.connection:
            self.connection.send(message)


