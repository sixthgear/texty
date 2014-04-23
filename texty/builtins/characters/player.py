from texty.builtins.characters import Character
from texty.builtins.characters import body
from texty.builtins.characters.body import PARTS
from texty.util import objectlist
from collections import OrderedDict


class Player(Character):

    attributes = 'player'

    def __init__(self, name, room=None, connection=None):
        super(Player, self).__init__(name, room)
        # players are associated with a server connection
        self.connection = connection
        self.occupation = 'Former Computer Programmer'
        # self.body = objectlist(self.__class__.body)
        self.status = 1

    def on_connect(self): pass
    def on_reconnect(self): pass
    def on_disconnect(self): pass

    def send(self, message):
        """
        Write a message to this player
        """
        if self.connection:
            self.connection.send(message)

    def sidebar(self):
        """
        send sidebar update
        """

        inv = []

        for x in self.inventory:
            inv.append({
                'type': '',
                'name': x.shortname,
                'description': x.description,
                'icon': x.icon
            })

        eq = OrderedDict((PARTS.DESC[x], y.shortname if y else '-') for x,y in self.eq_map.items())

        character = {
            'name': self.name,
            'occupation': self.occupation,
            'status': [
                {'level': 'high', 'text': 'You feel cold,', 'icon': 'fa-frown-o'},
                {'level': 'med', 'text': 'You feel hungry.', 'icon': 'fa-cutlery'}
            ],
            'equipment': eq,
            # 'hands': hands,
            'pack': {
                'name': '-',
                'capacity': 0,
                'amount': 0,
            },
            'inventory': inv,

        }
        self.send({'type': 'character', 'character': character})
