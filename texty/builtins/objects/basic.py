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
    keywords = 'box'
    icon = 'fa-briefcase'

class Equipable(Portable):
    attributes = 'equipable'

class Weapon(Equipable):
    keywords = 'weapon'
    attributes = 'wieldable'
    rate = 1 # per second
    range = 1 # feet
    weight = 5
    icon = 'fa-magic'

class RangedWeapon(Weapon):
    keywords = 'gun'
    attributes = 'loadable'
    capacity = 10 # rounds
    range = 20 # feet
    def __init__(self):
        self.ammo = None

class Rifle(RangedWeapon):
    keywords = 'rifle'

class SubMachineGun(RangedWeapon):
    keywords = 'smg machinegun'

class Shotgun(RangedWeapon):
    keywords = 'shotgun'

class MeleeWeapon(Weapon):
    keywords = 'melee'
    attributes = 'melee'
    rate = 1 # per second
    range = 1 # feet
    damage = 100 # per hit
    icon = 'fa-wrench'

class Explosive(Portable):
    keywords = 'explosive'
    attributes = 'explosive'
    range = 1 # feet
    ordinance = 10 # tons
    timer = 10 # seconds
    weight = 2
    pull_message = "%s %s the pin on %s."
    icon = 'fa-asterisk'

class Grenade(Explosive):
    keywords = 'grenade'

class Ammo(Portable):
    keywords = 'ammo ammunition'
    attributes = 'ammo'
    fits = () # tuple of weapons this ammo wil work with
    damage = 100 # per hit
    capacity = 10 # rounds
    icon = 'fa-tablet'

    def __init__(self):
        self.capacity = self.__class__.capacity
