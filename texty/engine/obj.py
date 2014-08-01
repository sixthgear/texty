from texty.util.objectlist import ObjectList
from texty.engine.parser import parser
from texty.engine.events import EventDispatcher

class ObjectMeta(type):
    """
    The almighty "Object Metaclass".
    Used to combine nouns, adjectives and attributes from parent classes.
    Also adds every object class into a global registry that can
    be used for admin commands. If you aren't familiar with Python
    meta-programming, there be a few dragons here.
    """
    def __new__(cls, name, bases, attrs):

        parents = [b for b in bases if isinstance(b, ObjectMeta)]

        # Don't do anything special unless this is a subclass BaseObject.
        if not parents:
            return type.__new__(cls, name, bases, attrs)

        # Split noun, adjective and attribute strings into sets
        attrs['nouns']      = set(attrs.get('nouns', '').split())
        attrs['adjectives'] = set(attrs.get('adjectives', '').split())
        attrs['attributes'] = set(attrs.get('attributes', '').split())

        # Combine attributes from parent classes
        for b in bases:
            attrs['nouns'].update(b.nouns)
            attrs['adjectives'].update(b.adjectives)
            attrs['attributes'].update(b.attributes)

        # use docstring for name and description if none defined
        if attrs.get('__doc__') and (not attrs.get('description') or not attrs.get('name')):
            doc = attrs.get('__doc__').strip().split('---')
            attrs['name'] = doc[0].strip()
            attrs['description'] = str.join('', doc[1:]).strip()

        # derive shortname from name if none defined
        if attrs.get('name') and not attrs.get('shortname'):
            attrs['shortname'] = attrs.get('name').split()[0]

        # Create the class and add it to the registry
        # TODO: don't add abstract clases to the registry!
        new_class = type.__new__(cls, name, bases, attrs)
        parser.register_object(new_class)
        return new_class


class BaseObject(EventDispatcher, metaclass=ObjectMeta):
    """
    Base object
    """
    name = 'an object'
    shortname = 'Obj'
    description = 'This is a nice object.'
    icon = 'fa-briefcase'

    nouns = set()
    adjectives = set()
    attributes = {'object'}
    plural = False

    @property
    def display(self):
        return self.name

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

    def is_a(self, attr):
        attrs = set(attr.split())
        return attrs.issubset(self.attributes)

    def is_any(self, attr):
        attrs = set(attr.split())
        return len(attrs & self.attributes) > 0

    def allows(self, verbs):
        return True

    # state management methods
    def pop_state(self, *args, **kwargs):
        self.state[-1].exit()
        state = self.state.pop()
        print("POPPED STATE", self.name, state.__class__.__name__)
        if self.state:
            # print (kwargs)
            self.state[-1].enter(*args, **kwargs)

    def push_state(self, state, *args, **kwargs):
        if self.state:
            self.state[-1].exit()
        self.state.append(state(self))
        print("PUSHED STATE", self.name, state)
        self.state[-1].enter(*args, **kwargs)


    def replace_stack(self, state, *args, **kwargs):
        self.state = [state(self)]
        print("REPLACED STACK", self.name, state)
        self.state[-1].enter(*args, **kwargs)

    def update(self, tick):
        if self.state:
            self.state[-1].update()
