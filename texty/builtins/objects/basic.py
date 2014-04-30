"""
Basic Objects to inherit from.
"""
from texty.engine.obj import BaseObject
from texty.util.objectlist import ObjectList
from texty.util.exceptions import TextyException

class Container(BaseObject):
    """
    This object can hold other objects.
    """
    attributes  = 'container'
    contents    = []

    def __init__(self):
        # instantiate class templates for constants
        self.contents = ObjectList([x() for x in self.__class__.contents])

class Portable(BaseObject):
    """
    This object can be carried.
    """
    attributes  = 'portable'
    weight      = 1 # kg

class Box(Portable, Container):
    """
    """
    nouns       = 'box'
    icon        = 'fa-briefcase'

class Food(Portable):
    """
    This object can be eaten
    """
    attributes  = 'food'

    def eat(self):
        pass

class Equipable(Portable):
    """
    This object can be worn.
    """
    attributes  = 'equipable'
    fits        = ()

class Weapon(Equipable):
    """
    This object can be used to hurt things.
    """
    nouns       = 'weapon'
    attributes  = 'wieldable'
    # --
    rate        = 1 # per second
    range       = 1 # feet
    weight      = 5

class MeleeWeapon(Weapon):
    """
    This object can be used to hurt things from close-up.
    """
    attributes  = 'melee'
    icon        = 'icon-screwdriver'
    # --
    rate        = 1 # per second
    range       = 1 # feet
    damage      = 100 # per hit

class Explosive(Portable):
    """
    This object can be used to hurt things with explosive power.
    """
    nouns       = 'explosive'
    attributes  = 'explosive'
    icon        = 'icon-bomb'
    # --
    range       = 1 # feet
    ordinance   = 10 # tons
    timer       = 10 # seconds
    weight      = 2

class RangedWeapon(Weapon):
    """
    This object can be used to hurt things from a distance.
    """
    nouns       = 'gun'
    attributes  = 'loadable'
    icon        = 'icon-gun'
    # --
    capacity    = 10 # rounds
    range       = 20 # feet

    def __init__(self):
        self.ammo = None

    def load(self, ammo):
        """
        Put ammo in this thing.
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
        Remove ammo from this thing.
        """
        if not self.ammo:
            raise TextyException('{} is empty.'.format(self.name))
        ammo, self.ammo = self.ammo, None
        return ammo

    @property
    def contents(self):
        return getattr(self.ammo, 'contents', [])


class Ammo(Portable):
    """
    This object can be put it weapons.
    """
    nouns       = 'ammo ammunition'
    attributes  = 'ammo'
    icon        = 'icon-package'
    # --
    item        = 'round'
    fits        = () # tuple of weapons this ammo wil work with
    damage      = 100 # per hit
    capacity    = 10 # rounds

    @property
    def contents(self):
        """
        Fake contents.
        """
        a = BaseObject()
        s = 's' if self.amount != 1 else ''
        a.amount = self.amount
        a.plural = True
        a.icon = self.icon
        a.name = '{n} {item}{s}'.format(n=self.amount, item=self.item, s=s)
        return ObjectList([ a ])

    def __init__(self):
        self.amount = self.__class__.capacity
