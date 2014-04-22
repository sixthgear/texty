"""
Body Parts
"""
from texty.builtins.objects import BaseObject

class PARTS:
    BODY, LEGS, FEET, HEAD, ARMS, NECK, WAIST, SHOULDERS, FING_L, FING_R, HAND_L, HAND_R = range(12)
    DESC = {
        BODY:       'Body',
        LEGS:       'Legs',
        FEET:       'Feet',
        HEAD:       'Head',
        ARMS:       'Arms',
        NECK:       'Neck',
        WAIST:      'Waist',
        SHOULDERS:  'Shoulders',
        FING_L:     'L. Finger',
        FING_R:     'R. Finger',
        HAND_L:     'L. Hand',
        HAND_R:     'R. Hand',
    }

class BodyPart(BaseObject):
    attributes = 'bodypart'

class Body(BodyPart):
    """
    body
    """
    nouns = 'torso abdomen stomach'
    typ = PARTS.BODY

class Legs(BodyPart):
    """
    legs
    """
    nouns = 'leg'
    typ = PARTS.LEGS

class Feet(BodyPart):
    """
    feet
    """
    nouns = 'foot feet'
    typ = PARTS.FEET

class Head(BodyPart):
    """
    fat head
    """
    nouns = 'head'
    typ = PARTS.HEAD

class Arms(BodyPart):
    """
    arms
    """
    nouns = 'arm'
    typ = PARTS.ARMS

class Neck(BodyPart):
    """
    neck
    """
    nouns = 'neck'
    typ = PARTS.NECK

class Waist(BodyPart):
    """
    waist
    """
    nouns = 'waist'
    typ = PARTS.WAIST

class Shoulders(BodyPart):
    """
    shoulders
    """
    nouns = 'shoulder'
    typ = PARTS.SHOULDERS

class FingerLeft(BodyPart):
    """
    left finger
    """
    adjectives = 'left'
    nouns = 'finger'
    typ = PARTS.FING_L

class FingerRight(BodyPart):
    """
    right hand
    """
    adjectives = 'right'
    nouns = 'finger'
    typ = PARTS.FING_R

class HandLeft(BodyPart):
    """
    left hand
    """
    adjectives = 'left'
    nouns = 'hand'
    typ = PARTS.HAND_L

class HandRight(BodyPart):
    """
    right hand
    """
    adjectives = 'right'
    nouns = 'hand'
    typ = PARTS.HAND_R
