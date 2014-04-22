from texty.builtins.objects import BaseObject
from texty.builtins.characters import body
from texty.util import objectlist, english
from texty.engine.command import Command
from collections import OrderedDict

class Character(BaseObject):
    """
    Base character class, from which all other character classes are inherited from
    """
    name = 'Mr. Character'
    gender = 'N'
    occupation = None
    description = '{he} looks about as ready to kill you as anyone else here.'
    attributes = 'character'

    hitpoints = 100
    capacity = 20
    inventory = []
    equipment = {}

    def __init__(self, name = None, room=None):
        self.name = name or self.__class__.name
        self.description = english.resolve_single(self.__class__.description, self)
        self.hitpoints = self.__class__.hitpoints

        self.inventory = objectlist(self.__class__.inventory)

        self.equipment = objectlist(self.__class__.equipment)
        self.eq_map = OrderedDict(((x, None) for x in range(len(body.PARTS.DESC))))

        self.body = objectlist((
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

        self.room = room
        self.status = 1

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

        if not object.is_a('equipable'):
            raise SyntaxError('{} is not equipable.'.format(object.name))

        if not object.fits:
            raise SyntaxError('{} does not fit anything.'.format(object.name))

        if not parts:
            parts = object.fits

        for p in parts:

            if p not in object.fits:
                raise SyntaxError('It doesn\'t fit there.')

            if not self.eq_map.get(p):
                self.eq_map[p] = object
                self.equipment.append(object)
                return True

        raise SyntaxError('You already have something there.'.format(object.name))

    def unequip(self, object, parts=None):

        if not parts:
            parts = object.fits

        for part, eq in self.eq_map.iteritems():
            if eq == object:
                self.eq_map[part] = None
                self.equipment.remove(object)
                return True

        raise SyntaxError('Couldn\'t Unequip {}.'.format(object.name))



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

    def serialize(self):
        """
        Turn character into a dict suitable for sending to client as JSON.
        """
        data = dict()
        data['icon'] = {'N': 'fa-male', 'M': 'fa-male', 'F': 'fa-female', None: ''}[self.gender]
        if self.occupation:
            data['text'] = '<b>%s</b> the %s is here.' % (self.first, self.occupation.lower())
        else:
            data['text'] = '<b>%s</b> is here.' % (self.name)
        return data
