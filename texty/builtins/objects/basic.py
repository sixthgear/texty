"""
Basic Objects to inherit from.
"""
from texty.builtins.objects import BaseObject

class Container(BaseObject):
    """
    This object can hold other objects.
    """
    attributes = 'container'
    def __init__(self):
        self.contents = ObjectList()

class Portable(BaseObject):
    attributes = 'portable'
    weight = 1 # kg

class Box(Portable, Container):
    nouns = 'box'
    icon = 'fa-briefcase'

class Equipable(Portable):
    attributes = 'equipable'

class Weapon(Equipable):
    nouns = 'weapon'
    attributes = 'wieldable'
    rate = 1 # per second
    range = 1 # feet
    weight = 5
    icon = 'fa-magic'

class RangedWeapon(Weapon):
    nouns = 'gun'
    attributes = 'loadable'
    capacity = 10 # rounds
    range = 20 # feet
    def __init__(self):
        self.ammo = None

class Rifle(RangedWeapon):
    nouns = 'rifle'

class SubMachineGun(RangedWeapon):
    nouns = 'smg machinegun'

class Shotgun(RangedWeapon):
    nouns = 'shotgun'

class MeleeWeapon(Weapon):
    nouns = 'melee'
    attributes = 'melee'
    rate = 1 # per second
    range = 1 # feet
    damage = 100 # per hit
    icon = 'fa-wrench'

class Explosive(Portable):
    nouns = 'explosive'
    attributes = 'explosive'
    range = 1 # feet
    ordinance = 10 # tons
    timer = 10 # seconds
    weight = 2
    pull_message = "%s %s the pin on %s."
    icon = 'fa-asterisk'

class Grenade(Explosive):
    nouns = 'grenade'

class Ammo(Portable):
    nouns = 'ammo ammunition'
    attributes = 'ammo'
    fits = () # tuple of weapons this ammo wil work with
    damage = 100 # per hit
    capacity = 10 # rounds
    icon = 'fa-tablet'

    def __init__(self):
        self.capacity = self.__class__.capacity
