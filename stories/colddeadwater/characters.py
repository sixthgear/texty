from texty.builtins.characters import NPC
from texty.util.enums import EQ_PARTS
from . objects import FreeBSDshirt, RippedJeans, Burrito

class Bertram(NPC):
    """
    Bertram Bolshtein
    ---
    You look at Bertram, a thin, wiry figure with a kind face. He serves as the camp medic.
    """
    occupation = 'Medic'
    nouns = 'bertram medic man'
    adjectives = 'thin wiry kind'
    gender = 'M'


class Tank(NPC):
    """
    Tank
    ---
    Tank is a massive hulk of a man. You wouldn't want to cross him with his bare hands, let
    alone when he has access to the camp's armaments. If you want anything from the
    storage locker, you'll need to run it by him.
    """
    occupation = 'Weapons Keeper'
    nouns = 'tank man'
    adjectives = 'massive hulking'
    gender = 'M'


class DForsyth(NPC):
    """
    Davide Forsyth
    ---
    Holy shit, the renowned author of "Power Moves" is standing here, not taking Uber. He looks
    like he doesn't give a shit about zombies, the apocalypse, or anything. What a pro.
    """
    occupation = '10x Programmer'
    nouns = 'dforsyth davide forsyth programmer'
    gender = 'M'
    activity = 'not taking Uber'

    equipment = {
        EQ_PARTS.BODY:      FreeBSDshirt,
        EQ_PARTS.LEGS:      RippedJeans,
        EQ_PARTS.L_HAND:    Burrito,
    }


class Fenton(NPC):
    """
    Fenton
    ---
    Fenton looks pretty dumb.
    """
    occupation = 'retarded dog'
    nouns = 'fenton dog'
    adjectives = 'retarded'
    icon = 'icon-paw'
