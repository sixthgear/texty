from texty.util.exceptions import TextyException
from texty.builtins.objects import BaseObject
from texty.builtins.characters import body
from texty.util.enums import EQ_PARTS, CHAR_STATUS, CHAR_FLAG
from texty.util import objectlist, english
from texty.engine.command import Command
from collections import OrderedDict

class Character(BaseObject):
    """
    Base character class, from which all other character classes are inherited from
    """
    # info
    name            = 'Mr. Character'
    gender          = 'N'
    occupation      = ''
    description     = '{he} looks about as ready to kill you as anyone else here.'
    attributes      = 'character'
    # stats
    hp              = 100
    capacity        = 20
    # simple lists provide templates to instantiate
    inventory       = []
    equipment       = {}

    def __init__(self, name=None, room=None):

        # copy data from class on init. This lets us reset the character to
        # initial values if required by calling __init__ again.
        self.name = name or self.__class__.name
        self.description = english.resolve_single(self.__class__.description, self)
        self.hp = self.__class__.hp
        self.room = room
        self.status = CHAR_STATUS.NORMAL

        # instantiate classes from inventory list upon init.
        self.inventory = objectlist((x() for x in self.__class__.inventory))

        # equipment is the searchable object list containing everything the character is
        # currently wielding/wearing.
        self.equipment = objectlist()
        self.eq_map = OrderedDict(((x, None) for x in EQ_PARTS))

        # eq_map is the mapping from EQ_PARTS enum to the object.
        for eq, x in self.__class__.equipment.items():
            obj = x()
            self.equipment.append(obj)
            self.eq_map[eq] = obj

    @property
    def icon(self):
        if self.gender in ('M', 'N'):
            return 'fa-male'
        elif self.gender == 'F':
            return 'fa-female'
        else:
            return ''

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
        c.run()

    def send(self, message):
        """
        By default, do nothing. Not all characters are players (ie. they don't need to see output)
        """
        pass

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
        for p in parts:

            if p not in object.fits:
                raise TextyException('It doesn\'t fit there.')

            if not self.eq_map.get(p):
                self.eq_map[p] = object
                self.equipment.append(object)
                return True

        # tried to equip object in all supplied positions, didn't work.
        raise TextyException('You already have something there.'.format(object.name))

    def unequip(self, object, parts=None):
        """
        """
        if not parts:
            parts = object.fits

        for part, eq in self.eq_map.items():
            if eq == object:
                self.eq_map[part] = None
                self.equipment.remove(object)
                return True

        raise TextyException('Couldn\'t Unequip {}.'.format(object.name))


    def move_to(self, room):
        """
        Move this character to a different room. This can be called by command functions or as
        an internal call. The calling function is reponsible to send notifications.
        Use None to remove the player from all rooms.
        """
        # first remove this player from the rooms characters list
        if self.room and self in self.room.characters:
            self.room.characters.remove(self)
        # next change the players room reference, and then add to the new room's character list
        if room:
            self.room = room
            if self.is_a('player'):
                self.room.characters.insert(0, self)
            else:
                self.room.characters.append(self)

