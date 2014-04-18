"""
MONSTERS
"""
from texty.builtins.characters import Character

class Monster(Character):
    """
    Base Enemy class
    """
    keywords = 'enemy'
    attributes = 'character'
    hitpoints = 100

