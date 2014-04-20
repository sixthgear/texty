from texty.builtins.characters import NPC

class Bertram(NPC):
    name = 'Bertram Bolshtein'
    occupation = 'Medic'
    nouns = 'bertram medic man'
    adjectives = 'thin wiry kind'
    description = 'You look at Bertram, a thin, wiry figure with a kind face. He serves as the camp medic.'

class Tank(NPC):
    name = 'Tank, the weapons keeper'
    nouns = 'tank man'
    massive = 'massive hulking'
    description = "Tank is a massive hulk of a man. You wouldn't want to cross him with his bare hands, let "
    description += "alone when he has access to the camp's armaments. If you want anything from the "
    description += "storage locker, you'll need to run it by him."

