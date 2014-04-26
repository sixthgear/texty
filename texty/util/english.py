"""
Helper functions to make nice english output.
"""

from texty.util.enums import PRONOUN_TYPES

class PRONOUN:
    """
    Pronoun table to use in action descriptions.
    """

    TABLE = {
        #         SUB,   OBJ,    POS,    REF             # PRO,
        'Y':    ['you', 'you',  'your', 'yourself'],     # 'yours',
        'M':    ['he',  'him',  'his',  'hisself]'],     # 'his',
        'F':    ['she', 'her',  'her',  'herself]'],     # 'hers',
        'N':    ['it',  'it',   'its',  'itself'],       # 'its',
        None:   ['they' 'them', 'their','themself'],     # 'theirs',
    }

def pn_sub(char): return PRONOUN.TABLE[char.gender][PRONOUN_TYPES.SUB.value]
def pn_obj(char): return PRONOUN.TABLE[char.gender][PRONOUN_TYPES.OBJ.value]
def pn_pos(char): return PRONOUN.TABLE[char.gender][PRONOUN_TYPES.POS.value]
def pn_ref(char): return PRONOUN.TABLE[char.gender][PRONOUN_TYPES.REF.value]
def pn_plural_s(char): return '' if char.gender == 'Y' else 's'
def pn_plural_es(char): return '' if char.gender == 'Y' else 'es'

def resolve_single(subject, string, source=None):
    """
    """
    return string.format(
        name = subject.name,
        names = subject.name + "'s",
        He = pn_sub(subject).title(),
        he = pn_sub(subject),
        him = pn_obj(subject),
        his = pn_pos(subject),
        hisself = pn_ref(subject),
        s = pn_plural_s(subject),
        es = pn_plural_es(subject)
    )


def resolve_singular(string, subject, object, source=None):
    """
    Resolve a templated string referencing a single subject and object character.
    {sub} swing{sub_s} {sub_his} {weapon} wildly at {objs} head.
    The {weapon} misses {obj_his} head by mere inches. {obj} step{obj_s} back in surprise.
    """
    # if subject == source:
        # replace all subject lookups to 2nd person counterpart
    # if object == source:
        # replace all object lookups to 2nd person counterpart

    return string.format(
        sub = subject.name,
        subs = subject.name + "'s",
        sub_he = pn_sub(subject),
        sub_him = pn_obj(subject),
        sub_his = pn_pos(subject),
        sub_hisself = pn_ref(subject),
        sub_s = pn_plural_s(subject),
        sub_es = pn_plural_es(subject),

        obj = object.name,
        objs = object.name + "'s",
        obj_he = pn_sub(object),
        obj_him = pn_obj(object),
        obj_his = pn_pos(object),
        obj_hisself = pn_ref(object),
        obj_s = pn_plural_s(object),
        obj_es = pn_plural_es(object),
    )
