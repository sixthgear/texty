from collections import OrderedDict
from texty.builtins.characters import body
from texty.builtins.states.combat import RelaxedState
from texty.engine.command import Command
from texty.engine.obj import BaseObject
from texty.util import objectlist, english
from texty.util.enums import EQ_PARTS, CHAR_STATE, CHAR_FLAG
from texty.util.exceptions import TextyException

class Character(BaseObject):
    """
    Base character class, from which all other character classes are inherited from
    """
    # info
    name            = 'Mr. Character'
    gender          = 'N'
    occupation      = ''
    activity        = ''
    description     = '{He} looks about as ready to kill you as anyone else here.'
    attributes      = 'character'
    # stats
    hp              = 100
    capacity        = 20
    strength        = 0
    dexterity       = 0
    intelligence    = 0
    # simple lists provide templates to instantiate
    inventory       = []
    equipment       = {}

    def __init__(self, name=None, node=None):

        # copy data from class on init. This lets us reset the character to
        # initial values if required by calling __init__ again.
        self.name = name or self.__class__.name
        self.description = english.STR.T(self.__class__.description, subject=self)
        self.hp = self.__class__.hp

        self.node = node
        self.move_target = None
        self.current_dir = None

        # the state stacks!
        self.state = [RelaxedState(self)]

        # instantiate classes from inventory list upon init.
        self.inventory = objectlist((x() for x in self.__class__.inventory))

        # equipment is the searchable object list containing everything the character is
        # currently wielding/wearing.
        self.equipment = objectlist()

        # eq_map is the mapping from EQ_PARTS enum to the object.
        self.eq_map = OrderedDict(((x, None) for x in EQ_PARTS))

        for eq, x in self.__class__.equipment.items():
            obj = x()
            self.equipment.append(obj)
            self.eq_map[eq] = obj

        self.attributes = self.__class__.attributes.copy()
        self.activity = self.__class__.activity

    def pop_state(self):
        self.state[-1].exit()
        self.state.pop()
        if self.state:
            self.state[-1].enter()

    def push_state(self, state, *args, **kwargs):
        if self.state:
            self.state[-1].exit()
        self.state.append(state(self))
        self.state[-1].enter(*args, **kwargs)

    def replace_stack(self, state, *args, **kwargs):
        self.state = [state(self)]
        self.state[-1].enter(*args, **kwargs)

    def update(self, tick):
        if self.state:
            self.state[-1].update()


    @property
    def icon(self):
        if self.gender in ('M', 'N'):
            return 'icon-man'
        elif self.gender == 'F':
            return 'icon-woman'
        else:
            return ''

    @property
    def display(self):
        if self.occupation:
            return '{x.first} the {x.occupation}'.format(x=self)
        else:
            return '{x.name}'.format(x=self)

    @property
    def first(self):
        return self.name.split()[0].capitalize()

    @property
    def inv_weight(self):
        weight = 0
        for i in self.inventory:
            weight += i.weight
        return weight

    def do(self, command, echo=False):
        """
        Parse and execute a text command for this player.
        """
        c = Command(source=self, command=command, echo=echo)
        c.parse()
        c.run()

    def send(self, message):
        """
        By default, do nothing. Not all characters are players (ie. they don't need to see output)
        """
        pass

    def get(self, object, container):
        self.trigger('get', object=object, container=container)

    def drop(self, object, node):
        self.trigger('drop', object=object, node=node)

    def put(self, object, container):
        self.trigger('put', object=object, container=container)

    def give(self, object, character):
        self.trigger('put', object=object, character=character)

    def use(self, object):
        self.trigger('put', object=object)

    def eat(self, object):
        self.trigger('eat', object=object)

    def load(self, weapon=None, ammo=None):
        self.trigger('load', weapon=weapon, ammo=ammo)

    def unload(self, weapon=None):
        self.trigger('unload', weapon=weapon)

    def ready(self):
        self.trigger('ready')

    def target(self, character):
        self.trigger('target', character=character)

    def stop(self):
        self.trigger('stop')

    def flee(self):
        self.trigger('flee')

    def equip(self, object, parts=None):
        """
        Take reference to object and assign it to characters equipment slots.
        """
        # first check if this object is equipable
        if not object.is_a('equipable'):
            raise TextyException('{} is not equipable.'.format(object.name))

        # next make sure if it has defined a "fits" list.
        if not object.fits:
            raise TextyException('{} does not fit anything.'.format(object.name))

        # use the "fits" list if no specific parts specified
        if not parts:
            parts = object.fits

        # try each part
        for part in parts:

            if part not in object.fits:
                raise TextyException('It doesn\'t fit there.')

            if not self.eq_map.get(part):
                self.eq_map[part] = object
                self.equipment.append(object)
                self.trigger('equip', object=object, part=part)
                return True

        # tried to equip object in all supplied positions, didn't work.
        raise TextyException('You already have something there.'.format(object.name))

    def unequip(self, object, parts=None):
        """
        Take thing off
        """
        if not parts:
            parts = object.fits

        for part, eq in self.eq_map.items():
            if eq == object:
                self.eq_map[part] = None
                self.equipment.remove(object)
                self.trigger('unequip', object=object, part=part)
                return True

        raise TextyException('Couldn\'t Unequip {}.'.format(object.name))


    def move_continue(self):

        if self.current_dir:
            self.node.move_dir(self, self.current_dir)
            # self.send('A: travelling...')
        else:
            self.stop()

    def stop(self):
        self.move_target = None
        self.current_dir = None
        self.state[-1].on_stop()

    def move_toward(self, target, direction):
        self.move_target = target
        self.current_dir = direction
        self.state[-1].on_move()

    def move_to(self, node):
        """
        Move this character to a different node. This can be called by command functions or as
        an internal call. The calling function is reponsible to send notifications.
        Use None to remove the player from all rooms.
        """
        # first remove this player from the rooms characters list
        if self.node and self in self.node.characters:
            self.node.exit(self)
            # self.node.characters.remove(self)
        # next change the players node reference, and then add to the new node's character list
        if node:
            self.node = node
            if self.is_a('player'):
                # self.node.characters.insert(0, self)
                self.node.enter(self)
            else:
                self.node.enter(self)
                # self.node.characters.append(self)

