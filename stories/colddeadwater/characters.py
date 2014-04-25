from texty.builtins.characters import NPC

class Bertram(NPC):
    """
    Bertram Bolshtein
    ---
    You look at Bertram, a thin, wiry figure with a kind face. He serves as the camp medic.
    """
    occupation = 'Medic'
    nouns = 'bertram medic man'
    adjectives = 'thin wiry kind'


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
