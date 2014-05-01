from texty.util.objectlist import ObjectList
from texty.util.enums import DIRECTIONS as DIR
import enum
import itertools

class SENS(enum.Enum):
    PASS    = 0 # no restriction
    BLOCK   = 1 # allow to leave, but not enter
    KILL    = 2 # not allowed to enter or leave

class DIM(enum.Enum):
    PORTAL  = 0
    NODE    = 1
    EDGE    = 2
    FIELD   = 3

class Node:
    """
    |  [A]P[B]

    A Portal is a dimensionless connection between other nodes. It can be used as a door.

    | [N]

    A Node is a targetable point of navigation. It can have an Edge connected to one of its
    six directions, or a field on any of the four horizontal directions.

    | [A] - <E> - [B]

    An Edge is a one-dimensional connection between two nodes.
    Characters and objects may occupy any of the intervals.

    |       [C]
    |     .  .  .
    | [A] . {F} . [B]
    |     .  .  .
    |       [D]

    A Field is a two-dimensional grid of coordinates attached to one or more nodes.
    Characters and objects may occupy any of the grid intervals. Navigation commands can be targeted
    to the outlier nodes or the center of the field. Interaction commands will cause the character to
    travel to the location of the interaction.

    """

    OPP = {
        DIR.NORTH:  DIR.SOUTH,
        DIR.SOUTH:  DIR.NORTH,
        DIR.EAST:   DIR.WEST,
        DIR.WEST:   DIR.EAST,
        DIR.UP:     DIR.DOWN,
        DIR.DOWN:   DIR.UP,
    }

    def __init__(self, name='', width=1, height=1, id=None):
        """
        Initialize this node.
        """
        self.name = name
        self.width = width
        self.height = height
        self.id = id
        self.intro = ''
        self.description = ''

        self.neighbors = {}             # DIR: Node
        self.characters = ObjectList()  # Characters contained in this Node
        self.objects = ObjectList()     # Objects contained in the Node
        self.interval = {}              # Char/Obj: Interval()

        self.targetable = id != None


        # allow vision to pass through this node by default
        # it might be useful to cause PORTAL type nodes to block vision, such as doors
        self.vision = SENS.PASS
        self.sounds = SENS.PASS

        if width == 0 or height == 0:
            self.type = DIM.PORTAL
        elif width == 1 and height == 1:
            self.type = DIM.NODE
        elif width == 1 or height == 1:
            self.type = DIM.EDGE
        else:
            self.type = DIM.FIELD

    def __repr__(self):
        return 'Node {n.id} {n.type.name} {n.name} {n.width}x{n.height}'.format(n=self)

    def connect(self, others):
        """
        Connect this node to one or more other nodes.
        """
        self.neighbors.update(others)
        for d, other in others.items():
            other.neighbors.update({self.OPP[d]: self})

    def enter(self, object, side):
        """
        Place an object into this node.
        TODO: event notifications
        """

        # portals may not be entered, except to pass object to their opposite connection
        if self.type == DIM.PORTAL:
            # pass thru to next node
            pass

        # set correct interval
        if side == DIR.NORTH:
            self.interval[object] = (0, -(self.height/2))
        elif side == DIR.SOUTH:
            self.interval[object] = (0, (self.height/2))
        elif side == DIR.WEST:
            self.interval[object] = (-(self.width/2), 0)
        elif side == DIR.EAST:
            self.interval[object] = ((self.width/2), 0)

        # append object to appropriate list
        if object.is_a('character'):
            self.characters.append(object)
        else:
            self.objects.append(object)

    def move(self, object, interval):
        """
        Move an object within this node.
        TODO: event notifications
        """
        self.interval[object] = interval

    def exit(self, object):
        """
        Remove an object from this node.
        TODO: event notifications
        """
        del self.interval[object]
        if object.is_a('character'):
            self.characters.remove(object)
        else:
            self.objects.remove(object)

    def notify(self, message, interval=None):
        """
        Notify this node and its neighbors of an event.
        """
        pass

    def nearby_targets(self, direction=None):
        """
        Return a dict of direction-neighbor  that can be targetted by navigation commands.
        This will typically skip edges, and some portals, but never nodes or fields.
        """
        targets = {}
        for d, n in self.neighbors.items():
            if direction and direction != d:
                continue
            elif n.targetable:
                targets.update({d: n})
            else:
                targets.update(n.nearby_targets(d))

        return targets


    def visible(self, distance=10, direction=None, position=0):
        """
        Find all CHARACTERS visible from this node.
        """
        closed = set()
        queue = [(self, 0, direction, position)]
        result = []

        while queue:
            # process next item in queue
            src, dist, dir, pos = queue.pop(0)
            # make sure we dont check the same thing twice
            closed.add(src)

            # return all objects in this node
            for c in src.characters:
                result.append((c, dist, dir))

            # now expand neighbors
            for d, neighbor in src.neighbors.items():

                # already seen this one
                if neighbor in closed:
                    continue

                # doesn't lie in a straight line from source
                if dir and dir != d:
                    continue

                # calculate total distance of next neighbor
                if d in (DIR.WEST, DIR.EAST):
                    n_dist = dist + src.width

                elif d in (DIR.NORTH, DIR.SOUTH):
                    n_dist = dist + src.height

                elif d in (DIR.UP, DIR.DOWN):
                    n_dist = dist + 1

                if n_dist <= distance:
                    queue.append((neighbor, n_dist, d, 0))


        return sorted(result, key=lambda x: x[1])

    @property
    def n(self): return self.neighbors[DIR.NORTH]
    @property
    def s(self): return self.neighbors[DIR.SOUTH]
    @property
    def e(self): return self.neighbors[DIR.EAST]
    @property
    def w(self): return self.neighbors[DIR.WEST]

    @property
    def exits(self):
        return self.nearby_targets()

    @property
    def contents(self):
        return self.characters + self.objects

    def sort(self):
        self.objects.sort(key=lambda i: (i.icon, i.shortname))

    def send(self, message, source=None):
        """
        Send a message to everyone in the room (besides source).
        """
        for c in self.characters:
            if c == source: continue
            c.send(message)

    @property
    def nearby(self):
        desc = self.exit_description()
        if desc:
            return "You see {desc}.".format(desc=desc)
        else:
            return ""

    def exit_description(self):

        directions = {
            DIR.WEST:   'to the <i>west</i>',
            DIR.NORTH:  'to the <i>north</i>',
            DIR.EAST:   'to the <i>east</i>',
            DIR.SOUTH:  'to the <i>south</i>',
            DIR.DOWN:   'below you',
            DIR.UP:     'above you',
        }

        exit_desc = []
        for d, exit in self.exits.items():
            exit_desc.append("the <b>{}</b> {}".format(exit.name.lower() or 'something', directions[d]))

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



