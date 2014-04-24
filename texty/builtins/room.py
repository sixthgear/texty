from texty.builtins.objects import BaseObject
from texty.util.objectlist import ObjectList

class Room(BaseObject):
    """
    Room object
    """
    def __init__(self, id, title='', description=''):
        # basic information
        self.id = id
        self.title = title
        self.intro = ''
        self.description = description
        # exits is a dict mapping from direction names to room references
        self.exits = {}
        # these are Texty ObjectLists so that we can search for them easier in
        # the noun resolution phase of the parser with keywords, scopes and attribures
        self.characters = ObjectList()
        self.objects = ObjectList()

    def send(self, message, source=None):
        """
        Send a message to everyone in the room (besides source).
        """
        for c in self.characters:
            if c == source: continue
            c.send(message)

    def __repr__(self):
        return self.id

    @property
    def contents(self):
        return self.characters + self.objects
