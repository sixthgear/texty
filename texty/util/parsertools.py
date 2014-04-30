from itertools import tee, islice, zip_longest
from texty.util.enums import TOK
import collections

def lookahead(some_iterable, window=1):
    items, nexts = tee(some_iterable, 2)
    nexts = islice(nexts, window, None)
    return zip_longest(items, nexts)

class VOCAB:
    """
    Dictionary of accepted symbols.
    """
    # special set that is updated as players enter or leave the game
    characters      =   collections.Counter()

    # filled in dyamically
    verbs           =   set()
    nouns           =   set()
    adjectives      =   set()
    phrasals        =   set()
    commands        =   {'say', 'yell', 'shout', 'tell', '"', 'broadcast', 'admin', 'warp'}

    # set of reserved nouns
    reserved        =   {'me', 'room', 'myself', 'self', 'floor', 'ground'}

    superlatives    =   {'best', 'worst', 'closest', 'furthest', 'biggest', 'largest', 'smallest', 'dumbest'}

    prepositions    =   {'above', 'against', 'ahead', 'around', 'at', 'behind', 'below'}
    prepositions   |=   {'for', 'from', 'in', 'inside', 'into', 'off', 'on', 'out', 'outside', 'over'}
    prepositions   |=   {'through', 'to', 'toward', 'under', 'upon', 'using', 'with'}

    indefinites     =   {'a', 'an', 'any'}
    specifics       =   {'my', 'the'}

    quantifiers     =   {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}
    quantifiers    |=   {'one', 'two', 'three', 'fouth', 'five', 'six', 'seven', 'eight', 'nine', 'ten '}
    quantifiers    |=   {'all', 'both', 'each', 'every', 'everything'}

    ordinals        =   {'first', 'second', 'third', 'fourth', 'fifth', 'sixth'}
    ordinals       |=   {'seventh', 'eighth', 'nineth', 'ninth', 'tenth', 'last'}
    ordinals       |=   {'1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'}


class Token(object):
    """
    Data type for a processed symbol from the command.
    """

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __repr__(self):
        if self.val:
            return '%s: "%s"' % (self.typ.name, self.val)
        else:
            return self.typ

