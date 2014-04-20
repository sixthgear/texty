from texty.util.objectlist import ObjectList
from texty.engine.parser import parser

class MetaObject(type):
    """
    The almighty "Object Metaclass".
    Used to combine nouns, adjectives and attributes from parent classes.
    Also adds every object class into a global registry that can
    be used for admin commands. If you aren't familiar with Python
    meta-programming, there be a few dragons here.
    """
    def __new__(cls, name, bases, attrs):

        parents = [b for b in bases if isinstance(b, MetaObject)]
        if not parents:
            # Don't do anything special unless this is a subclass BaseObject.
            # Thanks Django!
            return type.__new__(cls, name, bases, attrs)

        # Split nouns string into a list
        if attrs.has_key('nouns'):
            attrs['nouns'] = attrs['nouns'].split()
        else:
            attrs['nouns'] = []

        # Split adjectives string into a set
        if attrs.has_key('adjectives'):
            attrs['adjectives'] = set(attrs['adjectives'].split())
        else:
            attrs['adjectives'] = set()

        # Split attribues string into a set
        if attrs.has_key('attributes'):
            attrs['attributes'] = set(attrs['attributes'].split())
        else:
            attrs['attributes'] = set()


        # Combine attributes from parent classes
        for b in bases:
            if hasattr(b, 'nouns'):
                attrs['nouns'].extend(b.nouns)

            if hasattr(b, 'attributes'):
                attrs['attributes'].update(b.attributes)

            if hasattr(b, 'adjectives'):
                attrs['adjectives'].update(b.adjectives)

        # Create the class and add it to the registry
        # TODO: don't add abstract clases to the registry!
        new_class = type.__new__(cls, name, bases, attrs)
        parser.register_object(new_class)
        return new_class


class BaseObject(object):
    """
    Base object
    """
    __metaclass__ = MetaObject

    name = 'an object'
    shortname = 'Obj'
    description = 'This is a nice object.'
    icon = 'fa-briefcase'

    nouns = []
    attributes = set(['object'])
    adjectives = set()

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

    def is_a(self, attr):
        return attr in self.attributes

    def serialize(self):
        return {'icon': self.icon, 'text': '<b>%s</b> is here.' % self.name}


