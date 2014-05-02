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

        'excel_file':           './stories/colddeadwater/data/map.xlsx',
        'map_file':             './stories/colddeadwater/data/map.csv',
        'node_file':            './stories/colddeadwater/data/nodes.csv',

        'safe_prefix':          'HQ',
        'start_at':             'HQ8',
        'armory_at':            'HQ4'
    }

    def initialize(self):
        """
        Setup game
        """

        d  = list()
        d += [MP5] * 10
        d += [Model70] * 10
        d += [Model870] * 10
        d += [M1911] * 10
        d += [Magazine9mm] * 40
        d += [Magazine45ACP] * 40
        d += [Box12Gauge] * 40
        d += [BoxRifleCartridges] * 30
        d += [Crowbar] * 20
        d += [Frag] * 20
        d += [Radio] * 10
        d += [ClifBar] * 20
        d += [Burrito] * 20
        d += [CivilWarTrenchcoat] * 5
        d += [LeatherBoots] * 5
        d += [MotorcycleHelmet] * 5
        d += [RippedJeans] * 10
        d += [Tshirt] * 15
        d += [FreeBSDshirt] * 5
        d += [VibramFivefinger] * 2
        d += [Crate] * 5

        # distribute items
        for i in range(int(len(self.map.nodes) * 0.65)):
            node = random.choice(list(self.map.nodes.values()))
            node.objects.append(random.choice(d)())

        # distribute zombies
        for i in range(int(len(self.map.nodes) * 0.66)):
            node = random.choice(list(self.map.nodes.values()))
            if not node.id.startswith(self.options.get('safe_prefix')):
                z = enemies.Zombie()
                z.move_to(node)

        # make room items nice
        for node in self.map.nodes.values():
            node.sort()



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
