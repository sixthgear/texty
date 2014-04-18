from texty.builtins.objects import BaseObject
from texty.util import objectlist

class Character(BaseObject):
    """
    Base character class, from which all other character classes are inherited from
    """
    name = 'Mr. Character'
    gender = 'N'
    occupation = None
    description = '{he} looks as ready to kill you as anyone else here.'
    attributes = 'character'

    hitpoints = 100
    capacity = 20
    inventory = []
    equipment = {}

    def __init__(self, name = None, room=None):
        self.name = name or self.__class__.name
        self.description = self.__class__.description
        self.hitpoints = self.__class__.hitpoints
        self.inventory = objectlist(self.__class__.inventory)
        self.equipment = objectlist(self.__class__.equipment)
        self.room = room

    @property
    def first(self):
        return self.name.split()[0].capitalize()

    @property
    def inv_weight(self):
        weight = 0
        for i in self.inventory:
            weight += i.weight
        return weight

    def do(self, command):
        pass

    def send(self, message):
        pass

    def move_to(self, room):
        """
        Move this character to a different room. This can be called by command functions or as
        an internal call. The calling function is reponsible to send notifications.
        """
        if self.room and self in self.room.characters:
            self.room.characters.remove(self)

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
