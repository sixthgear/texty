from texty.builtins.characters import Character
from texty.builtins.characters import body
# from texty.builtins.characters.body import PARTS
from texty.util.enums import EQ_PARTS
from texty.util import objectlist
from collections import OrderedDict


class Player(Character):

    attributes = 'player'

    def __init__(self, name, room=None, connection=None):
        super(Player, self).__init__(name, room)
        # players are associated with a server connection
        self.connection = connection
        self.occupation = 'Former Computer Programmer'
        self.status = 1

        # take a copy, since we modify this directly and don't want to change nouns
        # for everyone!
        self.nouns = self.__class__.nouns.copy()

    def on_connect(self): pass
    def on_reconnect(self): pass
    def on_disconnect(self): pass

    def send(self, message):
        """
        Write a message to this player
        """
        if self.connection:
            self.connection.send(message)


