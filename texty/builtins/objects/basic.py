"""
Basic Objects to inherit from.
"""
from texty.builtins.objects import BaseObject
from texty.util.objectlist import ObjectList
from texty.util.exceptions import TextyException

class Container(BaseObject):
    """
    This object can hold other objects.
    """
    attributes = 'container'

    def __init__(self):
        self.contents = ObjectList([x() for x in self.__class__.contents])

class Portable(BaseObject):
    attributes = 'portable'
    weight = 1 # kg

class Box(Portable, Container):
    nouns = 'box'
    icon = 'fa-briefcase'

class Equipable(Portable):
    attributes = 'equipable'
    fits = ()

class Weapon(Equipable):
    nouns = 'weapon'
    attributes = 'wieldable'
    rate = 1 # per second
    range = 1 # feet
    weight = 5

class RangedWeapon(Weapon):
    nouns = 'gun'
    attributes = 'loadable'
    capacity = 10 # rounds
    range = 20 # feet
    icon = 'icon-gun'

    def __init__(self):
        self.ammo = None

    def load(self, ammo):
        """
        """
        if not ammo.is_a('ammo'):
            raise TextyException('{} is not ammunition.'.format(ammo.name))
        if not hasattr(ammo, 'fits') or self.__class__ not in ammo.fits:
            raise TextyException('{} doesn\'t fit in {}.'.format(ammo.name, self.name))
        if self.ammo:
            raise TextyException('{} is already loaded.'.format(self.name))
        self.ammo = ammo
        return True

    def unload(self):
        """
        """
        if not self.ammo:
            raise TextyException('{} is empty.'.format(self.name))
        ammo, self.ammo = self.ammo, None
        return ammo

    @property
    def contents(self):
        if self.ammo:
            return self.ammo.contents
        else:
            return []


class Rifle(RangedWeapon):
    nouns = 'rifle'

class SubMachineGun(RangedWeapon):
    nouns = 'smg machinegun'

class Shotgun(RangedWeapon):
    nouns = 'shotgun'

class MeleeWeapon(Weapon):
    # nouns = 'melee'
    attributes = 'melee'
    rate = 1 # per second
    range = 1 # feet
    damage = 100 # per hit
    icon = 'icon-screwdriver'

class Explosive(Portable):
    nouns = 'explosive'
    attributes = 'explosive'
    range = 1 # feet
    ordinance = 10 # tons
    timer = 10 # seconds
    weight = 2
    pull_message = "%s %s the pin on %s."
    icon = 'icon-bomb'

class Grenade(Explosive):
    nouns = 'grenade'

class Ammo(Portable):

    nouns = 'ammo ammunition'
    attributes = 'ammo'
    item = 'ammo'
    fits = () # tuple of weapons this ammo wil work with
    damage = 100 # per hit
    capacity = 10 # rounds
    icon = 'icon-package'

    @property
    def contents(self):
        a = BaseObject()
        s = 's' if self.amount != 1 else ''
        a.name = '{n} {item}{s}'.format(n=self.amount, item=self.item, s=s)
        return ObjectList([ a ])

    def __init__(self):
        self.amount = self.__class__.capacity
