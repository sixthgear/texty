from texty.util import english
from texty.util.files import construct_name, construct_occupation
from texty.builtins.story import Story

from colddeadwater.objects import *
from colddeadwater import commands
from colddeadwater import characters
from colddeadwater import enemies

import random

class ColdDeadWater(Story):
    """
    You suddenly discover that you are conscious. Darkness envelops you. You struggle to
    remember anything, even your own name.

    Slowly, you begin to remember.
    """

    __name__ = 'Cold Dead Water'
    __version__ = '0.0.1'

    options = {
        'map_file':     './stories/colddeadwater/data/map.csv',
        'room_file':    './stories/colddeadwater/data/rooms.csv',
        'start_at':     'A8'
    }

    def clean(self):
        """
        Reset map and characters
        """
        players = []
        for id, room in self.map.rooms.iteritems():
            players += [c for c in room.characters if c.is_a('player')]
            room.characters = []
            room.objects = []

        self.initialize()

        for p in players:
            p.send('A:Game is resetting.')
            p.move_to(self.starting_room)
            p.do('wakeup')

    def initialize(self):
        """
        Setup game
        """
        # create starting area NPCs
        characters.Bertram().move_to(self.starting_room)
        characters.Tank().move_to(self.map.rooms['A4'])

        # distribute starting area equipment
        for o in [Radio, Model70, MP5, BoxRifleCartridges, Magazine9mm, Magazine9mm, Crowbar]:
            self.starting_room.objects.append(o())

        crate = Crate()
        crate.contents += [PowerMoves(), PowerMoves(), PowerMoves(), PowerMoves(), PowerMoves(), PowerMoves()]

        self.starting_room.objects.append(crate)

        for o in [objects.Frag(), objects.Frag()]:
            self.map.rooms['A4'].objects.append(o)

        # distribute zombies
        for i in range(100):
            room = random.choice(self.map.rooms.values())
            if not room.id.startswith('A'):
                z = enemies.Zombie()
                z.move_to(room)


        for i in range(400):
            room = random.choice(self.map.rooms.values())
            if room.id.startswith('A'):
                i = random.choice((
                    ClifBar, ClifBar, ClifBar, ClifBar, ClifBar,
                    VibramFivefinger,
                    LeatherBoots, LeatherBoots, LeatherBoots,
                    MotorcycleHelmet, MotorcycleHelmet,
                    Tshirt, Tshirt, Tshirt,
                    RippedJeans, RippedJeans, RippedJeans,
                    CivilWarTrenchcoat,
                    BoxRifleCartridges, BoxRifleCartridges, BoxRifleCartridges, BoxRifleCartridges,
                    Model70,
                    MP5,
                    Magazine9mm, Magazine9mm, Magazine9mm, Magazine9mm, Magazine9mm, Magazine9mm, Magazine9mm, Magazine9mm, Magazine9mm,
                    Radio,
                    Frag, Frag,
                    Crowbar))()
                room.objects.append(i)

        for room in self.map.rooms.values():
            room.objects.sort(key=lambda i: (i.icon, i.shortname))


    def on_player_connect(self, player):
        """
        Start a player
        """
        # wakeup command, move player to Bertrams tent and introduce them
        player.gender = random.choice(['M', 'F'])
        player.name = construct_name(player.gender)
        player.occupation = construct_occupation()
        player.nouns.update(set(player.name.lower().split()))
        player.description = english.resolve_single(player.__class__.description, player)

        player.do('wakeup')
        # player.inventory += [PowerMoves(), objects.Frag()]
        # player.equip(RippedJeans())
        # player.equip(Tshirt())
        # player.equip(MP5())

        player.sidebar()

        return player

    def on_player_disconnect(self, player):

        # remove from room in firey blast
        player.do('combust')



storyclass = ColdDeadWater

