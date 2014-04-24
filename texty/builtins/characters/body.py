"""
Body Parts
"""
from texty.engine.obj import BaseObject
from texty.util.enums import EQ_PARTS


class BodyPart(BaseObject):
    attributes = 'bodypart'

class Body(BodyPart):
    """
    body
    """
    nouns = 'torso abdomen stomach'
    typ = EQ_PARTS.BODY

class Legs(BodyPart):
    """
    legs
    """
    nouns = 'leg'
    typ = EQ_PARTS.LEGS

class Feet(BodyPart):
    """
    feet
    """
    nouns = 'foot feet'
    typ = EQ_PARTS.FEET

class Head(BodyPart):
    """
    fat head
    """
    nouns = 'head'
    typ = EQ_PARTS.HEAD

class Arms(BodyPart):
    """
    arms
    """
    nouns = 'arm'
    typ = EQ_PARTS.ARMS

class Neck(BodyPart):
    """
    neck
    """
    nouns = 'neck'
    typ = EQ_PARTS.NECK

class Waist(BodyPart):
    """
    waist
    """
    nouns = 'waist'
    typ = EQ_PARTS.WAIST

class Shoulders(BodyPart):
    """
    shoulders
    """
    nouns = 'shoulder'
    typ = EQ_PARTS.SHOULDERS

class FingerLeft(BodyPart):
    """
    left finger
    """
    adjectives = 'left'
    nouns = 'finger'
    typ = EQ_PARTS.L_FINGER

class FingerRight(BodyPart):
    """
    right hand
    """
    adjectives = 'right'
    nouns = 'finger'
    typ = EQ_PARTS.R_FINGER

class HandLeft(BodyPart):
    """
    left hand
    """
    adjectives = 'left'
    nouns = 'hand'
    typ = EQ_PARTS.L_HAND

class HandRight(BodyPart):
    """
    right hand
    """
    adjectives = 'right'
    nouns = 'hand'
    typ = EQ_PARTS.R_HAND
