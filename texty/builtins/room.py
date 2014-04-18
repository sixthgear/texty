from texty.builtins.objects import BaseObject
from texty.util.objectlist import ObjectList
from texty.util.searchdict import SearchDict

class Room(BaseObject):
    """
    Room object
    """
    def __init__(self, id, title='', description=''):
        self.id = id
        self.title = title
        self.description = description
        self.exits = SearchDict()
        self.characters = ObjectList()
        self.objects = ObjectList()

    def send(self, message, source=None):
        for c in self.characters:
            if c == source: continue
            c.send(message)

    def __repr__(self):
        return self.id

