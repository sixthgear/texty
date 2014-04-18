"""
Body Parts
"""
from texty.builtins.objects import BaseObject

class BodyPart(BaseObject):
    attributes = 'body'

class Head(BodyPart):
    keywords = 'head'

class LeftArm(BodyPart):
    keywords = 'left arm'

class RightArm(BodyPart):
    keywords = 'right arm'

class LeftHand(BodyPart):
    keywords = 'left hand'

class RightHand(BodyPart):
    keywords = 'right hand'

class LeftLeg(BodyPart):
    keywords = 'left leg'

class RightLeg(BodyPart):
    keywords = 'right leg'

class LeftFoot(BodyPart):
    keywords = 'left foot'

class RightFoot(BodyPart):
    keywords = 'right foot'

class Torso(BodyPart):
    keywords = 'torso abdomen stomach'

