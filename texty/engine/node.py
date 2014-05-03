from texty.util.objectlist import ObjectList
from texty.util.enums import DIRECTIONS as DIR
from texty.engine.obj import BaseObject
import enum
import itertools

DIR_ENG = {
    DIR.WEST:   'to the <i>west</i>',
    DIR.NORTH:  'to the <i>north</i>',
    DIR.EAST:   'to the <i>east</i>',
    DIR.SOUTH:  'to the <i>south</i>',
    DIR.DOWN:   'below you',
    DIR.UP:     'above you',
}

OPP = {
    DIR.NORTH:  DIR.SOUTH,
    DIR.SOUTH:  DIR.NORTH,
    DIR.EAST:   DIR.WEST,
    DIR.WEST:   DIR.EAST,
    DIR.UP:     DIR.DOWN,
    DIR.DOWN:   DIR.UP,
}

class SENS(enum.Enum):
    PASS    = 0     # no restriction
    BLOCK   = 1     # allow to leave, but not enter
    KILL    = 2     # not allowed to enter or leave

class DIM(enum.Enum):
    PORTAL  = 0
    NODE    = 1
    EDGE    = 2
    FIELD   = 3

class Node(BaseObject):
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

    attributes = 'node'


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

        self.min_x = -width//2 + 1
        self.max_x = width//2
        self.min_y = -height//2 + 1
        self.max_y = height//2

        # allow vision to pass through this node by default
        # it might be useful to cause PORTAL type nodes to block vision, such as doors
        self.vision = SENS.PASS
        self.sounds = SENS.PASS

        # automatically discern classifiction for this node
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

    def in_bounds(self, x, y):
        return y <= self.max_y and y >= self.min_y and x <= self.max_x and x >= self.min_x

    def connect(self, others):
        """
        Connect this node to one or more other nodes.
        """
        self.neighbors.update(others)
        for d, other in others.items():
            other.neighbors.update({OPP[d]: self})

    def enter(self, object, side=None):
        """
        Place an object into this node.
        TODO: event notifications
        """

        # when entering portals, pass object to their opposite connection
        if self.type == DIM.PORTAL and self.neighbors.get(OPP[side]):
            self.neighbors[OPP[side]].enter(object, side)
            return

        # portal has no opposite side
        elif self.type == DIM.PORTAL:
            return

        # set correct interval
        elif side == DIR.NORTH:
            self.interval[object] = (0, self.min_y)
        elif side == DIR.SOUTH:
            self.interval[object] = (0, self.max_y)
        elif side == DIR.WEST:
            self.interval[object] = (self.min_x, 0)
        elif side == DIR.EAST:
            self.interval[object] = (self.max_x, 0)
        elif side == DIR.UP:
            self.interval[object] = (0, self.min_y)
        elif side == DIR.DOWN:
            self.interval[object] = (0, self.max_y)
        else:
            # place in center
            self.interval[object] = (0, 0)

        # set object reference to this node
        object.node = self

        # append object to appropriate list
        if object.is_a('character'):
            self.characters.append(object)
        else:
            self.objects.append(object)

        self.trigger('enter', object=object, side=side)


    def exit(self, object, side=None):
        """
        Remove an object from this node.
        TODO: event notifications
        """
        del self.interval[object]
        if object.is_a('character'):
            self.characters.remove(object)
        else:
            self.objects.remove(object)

        self.trigger('exit', object=object, side=side)


    def move_to(self, object, interval):
        """
        Move an object to a specific interval in this node.
        TODO: event notifications
        """
        self.interval[object] = interval
        self.trigger('movement', object=object, to=interval)

    def move_dir(self, object, direction, distance=1):
        """
        Move an object within this node.
        TODO: event notifications
        """
        current = self.interval[object]

        if direction == DIR.NORTH:
            x, y = current[0], current[1] - distance
        elif direction == DIR.SOUTH:
            x, y = current[0], current[1] + distance
        elif direction == DIR.WEST:
            x, y = current[0] - distance, current[1]
        elif direction == DIR.EAST:
            x, y = current[0] + distance, current[1]
        elif direction == DIR.UP:
            x, y = current[0], current[1] - distance
        elif direction == DIR.DOWN:
            x, y = current[0], current[1] + distance
        else:
            x, y = current[0], current[1]

        # movement within bounds
        if self.in_bounds(x, y):
            self.move_to(object, (x, y))

        # move object to neighboring node
        elif direction in self.neighbors:
            new = self.neighbors[direction]
            self.exit(object, direction)
            new.enter(object, OPP[direction])

        # hit a wall
        else:
            pass


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

    def map(self, character=None):
        """
        Generate a map.
        """

    def visible(self, distance=10, direction=None, character=None):
        """
        Find all CHARACTERS visible from this node with an optional character to use position.
        """

        if self.vision == SENS.KILL:
            return []

        closed = set()
        result = []
        # enqueue self
        if character:
            position = self.interval[character]
        else:
            position = (0, 0)
        queue = [(self, 0, direction, position)]

        while queue:
            # process next item in queue
            src, dist, dir, pos = queue.pop(0)
            # make sure we dont check the same thing twice
            closed.add(src)
            # report all objects in this node
            for c in src.characters:
                # determine object position from current position
                i_pos = src.interval[c]
                delta = pos[0] - i_pos[0], pos[1] - i_pos[1]
                # manhattan distance
                i_dist = dist + (abs(delta[0]) + abs(delta[1]))
                # do distance check
                if i_dist > distance:
                    continue
                # determine correct direction to report
                if delta[0] < 0:
                    i_dir = DIR.WEST
                elif delta[0] > 0:
                    i_dir = DIR.EAST
                elif delta[1] < 0:
                    i_dir = DIR.SOUTH
                elif delta[1] > 0:
                    i_dir = DIR.NORTH
                elif i_dist == 0:
                    i_dir = None
                else:
                    i_dir = dir
                # report the object
                result.append((c, i_dist, i_dir))

            # now expand neighbors
            for d, neighbor in src.neighbors.items():
                # already seen this one
                if neighbor in closed:
                    continue
                # doesn't lie in a straight line from source
                if dir and dir != d:
                    continue
                # this node blocks vision
                if neighbor.vision != SENS.PASS:
                    continue
                # calculate total distance to next neighbor and starting position within it
                leaving_cost = 0 if src.type == DIM.PORTAL else 1
                if d == DIR.WEST:
                    n_dist = dist + (pos[0] - src.min_x) + leaving_cost
                    n_pos = (neighbor.max_x, 0)
                elif d == DIR.EAST:
                    n_dist = dist + (src.max_x - pos[0]) + leaving_cost
                    n_pos = (neighbor.min_x, 0)
                elif d == DIR.NORTH or d == DIR.UP:
                    n_dist = dist + (pos[1] - src.min_y) + leaving_cost
                    n_pos = (0, neighbor.max_y)
                elif d == DIR.SOUTH or d == DIR.DOWN:
                    n_dist = dist + (src.max_y - pos[1]) + leaving_cost
                    n_pos = (0, neighbor.min_y)
                else:
                    raise ValueError('Expected a direction in neighbors.')
                # enqueue this neighbor if we have vision range remaining for it
                if n_dist <= distance:
                    queue.append((neighbor, n_dist, d, n_pos))

        # return sorted list
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
        """
        Sort the objects in the room.
        """
        self.objects.sort(key=lambda i: (i.icon, i.shortname))

    def send(self, message, source=None):
        """
        Send a message to everyone in the node (besides source).
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
        """
        Return an english list of nearby targetable nodes.
        """
        exit_desc = []
        for d, exit in self.exits.items():
            exit_desc.append("<b>{}</b> {}".format(exit.name.lower() or 'something', DIR_ENG[d]))

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



