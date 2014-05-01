"""
MONSTERS
"""
from texty.engine.character import Character

class Monster(Character):
    """
    Base Enemy class
    """
    nouns = 'enemy'
    attributes = 'monster'
    hitpoints = 100
    icon = 'icon-skeletor'

