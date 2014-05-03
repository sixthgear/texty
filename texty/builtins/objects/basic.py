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

