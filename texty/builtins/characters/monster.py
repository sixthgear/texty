"""
MONSTERS
"""
from texty.builtins.characters import Character

class Monster(Character):
    """
    Base Enemy class
    """
    nouns = 'enemy'
    attributes = 'character'
    hitpoints = 100

