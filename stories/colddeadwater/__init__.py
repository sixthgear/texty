from texty.util import english
from texty.util import objectlist
from texty.util import serialize
from texty.util.files import construct_name, construct_occupation
from texty.engine.story import Story

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
        for id, room in self.map.rooms.items():
            players += [c for c in room.characters if c.is_a('player')]
            room.characters = objectlist()
            room.objects = objectlist()

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
        characters.DForsyth().move_to(self.starting_room)
        characters.Tank().move_to(self.map.rooms['A4'])

        # distribute starting area equipment
        self.starting_room.objects += [
            Radio(),
            Model70(),
            MP5(),
            BoxRifleCartridges(),
            Magazine9mm(),
            Magazine9mm(),
            Crowbar(),
            Crate(),
        ]

        self.map.rooms['A4'].objects += [
            Frag(),
            Frag(),
        ]

        d  = list()
        d += [MP5] * 10
        d += [Model70] * 10
        d += [Magazine9mm] * 30
        d += [BoxRifleCartridges] * 30
        d += [Crowbar] * 20
        d += [Frag] * 20
        d += [Radio] * 10
        d += [ClifBar] * 40
        d += [CivilWarTrenchcoat] * 5
        d += [LeatherBoots] * 5
        d += [MotorcycleHelmet] * 5
        d += [RippedJeans] * 10
        d += [Tshirt] * 15
        d += [VibramFivefinger] * 2
        d += [Crate] * 10

        for i in range(200):
            room = random.choice(list(self.map.rooms.values()))
            room.objects.append(random.choice(d)())

        # distribute zombies
        for i in range(100):
            room = random.choice(list(self.map.rooms.values()))
            if not room.id.startswith('A'):
                z = enemies.Zombie()
                z.move_to(room)

        for room in self.map.rooms.values():
            room.sort()


    def on_player_connect(self, player):
        """
        Start a player
        """
        # wakeup command, move player to Bertrams tent and introduce them
        player.gender = random.choice(['M', 'F'])
        player.name = construct_name(player.gender)
        player.occupation = construct_occupation()
        player.nouns.update(set(player.name.lower().split()))
        player.description = english.resolve_single(player, player.__class__.description)

        player.do('wakeup')

        player.send(serialize.full_character(player))

        return player

    def on_player_disconnect(self, player):

        # remove from room in firey blast
        player.do('combust')



storyclass = ColdDeadWater
