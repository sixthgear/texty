from texty.builtins.objects import BaseObject
from texty.util.objectlist import ObjectList
from texty.util.enums import DIRECTIONS as DIR


class Edge:
    """
    An Edge is a connection between Nodes.
    """
    def __init__(self, id, size, exits, name='', description=''):

        # basic information
        self.id = id
        self.title = name
        self.intro = ''
        self.description = description

        # flag whether this interval allows LOS
        self.los = True

        # exits is a dict mapping from direction names to room references
        self.exits = [
            #   direction: room
        ]

        # room reference to the left
        left = left
        # room reference to the right
        left = right

        # slots for characters and objects to occupy
        self.intervals = []
        for n in range(size):
            self.intervals.append({
                'characters': ObjectList(),
                'objects': ObjectList(),
            })

class Room(BaseObject):
    """
    Room object
    """

    attributes = 'room'

    def __init__(self, id, name='', description=''):
        # basic information
        self.id = id
        self.name = name
        self.intro = ''
        self.description = description
        # exits is a dict mapping from direction names to room references
        self.exits = {}
        self.edges = {}

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

    def sort(self):
        self.objects.sort(key=lambda i: (i.icon, i.shortname))

    def __repr__(self):
        return '%s:%s' % (self.id, self.name)

    @property
    def contents(self):
        return self.characters + self.objects

    @property
    def nearby(self):
        desc = self.exit_description()
        if desc:
            return "You see {desc}.".format(desc=desc)
        else:
            return ""

    def exit_description(self):

        directions = {
            DIR.WEST:   'to the west',
            DIR.NORTH:  'to the north',
            DIR.EAST:   'to the east',
            DIR.SOUTH:  'to the south',
            DIR.DOWN:   'below you',
            DIR.UP:     'above you',
        }

        exit_desc = []
        for d, exit in self.exits.items():
            exit_desc.append("{} {}".format(exit.name, directions[d]))

        if len(exit_desc) == 1:
            return exit_desc[0]
        elif len(exit_desc) == 2:
            return str.join(' and ', exit_desc[-2:])
        elif len(exit_desc) > 2:
            head = str.join(', ', exit_desc[:-2])
            tail = str.join(' and ', exit_desc[-2:])
            return str.join(', ', (head, tail))
        else:
            return None


