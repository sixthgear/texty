from texty.builtins.characters import Character
from texty.builtins.characters.body import *
from texty.engine.command import Command
from texty.util import objectlist
from collections import OrderedDict


class Player(Character):

    attributes = 'player'

    body = [
        Head(),
        Torso(),
        LeftArm(),
        LeftHand(),
        LeftLeg(),
        LeftFoot(),
        RightArm(),
        RightHand(),
        RightLeg(),
        RightFoot(),
    ]

    def __init__(self, name, room=None, connection=None):
        super(Player, self).__init__(name, room)
        # players are associated with a server connection
        self.connection = connection
        self.occupation = 'Former Computer Programmer'
        self.body = objectlist(self.__class__.body)
        self.status = 1

    def on_connect(self): pass
    def on_reconnect(self): pass
    def on_disconnect(self): pass

    def do(self, command, echo=False):
        c = Command(source=self, command=command, status=self.status, echo=echo)
        c.run()

    def send(self, message):
        if self.connection:
            self.connection.send(message)

    def sidebar(self):
        """
        send sidebar update
        """
        character = {
            'name': self.name,
            'occupation': self.occupation,
            'status': [
                {'level': 'high', 'text': 'You feel cold,', 'icon': 'fa-frown-o'},
                {'level': 'med', 'text': 'You feel hungry.', 'icon': 'fa-cutlery'}
            ],
            'equipment': OrderedDict((
                ('Body', 'Muddy T-shirt'),
                ('Legs', 'Jeans'),
                ('Feet', 'Sneakers'),
                ('Head', '-'),
                ('Arms', '-'),
                ('Neck', '-'),
                ('Waist', '-'),
                ('Shoulders', '-'),
                ('L. Finger', '-'),
                ('R. Finger', '-'),
            )),
            'hands': OrderedDict((
                ('L. Hand', {'name': '-'}),
                ('R. Hand', {'name': '-'}),
            )),
            'pack': {
                'name': '-',
                'capacity': 0,
                'amount': 0,
            },
            'inventory': [{'type': '', 'name': x.shortname, 'description': x.description, 'icon': x.icon} for x in self.inventory],

        }
        self.send({'type': 'character', 'character': character})
