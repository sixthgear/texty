import itertools
import enum

iota = itertools.count()
class CHAR_STATUS(enum.Enum):
    """
    Character Control State
    """
    LIMBO                       = next(iota)
    NORMAL                      = next(iota)
    FIGHTING                    = next(iota)
    RESTING                     = next(iota)
    SLEEPING                    = next(iota)
    INCAPACITATED               = next(iota)
    DEAD                        = next(iota)


iota = (2**x for x in itertools.count())
class CHAR_FLAG(enum.Enum):
    """
    Character Status Flags.
    """
    BLIND                       = next(iota)
    BLEEDING                    = next(iota)
    SLOW                        = next(iota)
    COLD                        = next(iota)
    HUNGRY                      = next(iota)
    SICK                        = next(iota)


iota = itertools.count()
class DIRECTIONS(enum.Enum):
    """
    Room exit directions
    """
    NORTH                       = next(iota)
    EAST                        = next(iota)
    SOUTH                       = next(iota)
    WEST                        = next(iota)
    UP                          = next(iota)
    DOWN                        = next(iota)


iota = itertools.count()
class SCOPE(enum.Enum):
    """
    Command-Object resolution scopes.
    """
    EQUIP                       = next(iota)
    INV                         = next(iota)
    BODY                        = next(iota)
    OBJ                         = next(iota)
    CHAR                        = next(iota)
    IN                          = next(iota)
    HAS                         = next(iota)
    ANY                         = next(iota)
    ROOM                        = next(iota)


iota = itertools.count()
class EQ_PARTS(enum.Enum):
    """
    Places you can equip.
    """
    BODY                        = next(iota)
    LEGS                        = next(iota)
    FEET                        = next(iota)
    HEAD                        = next(iota)
    ARMS                        = next(iota)
    NECK                        = next(iota)
    WAIST                       = next(iota)
    SHOULDERS                   = next(iota)
    L_FINGER                    = next(iota)
    R_FINGER                    = next(iota)
    L_HAND                      = next(iota)
    R_HAND                      = next(iota)


iota = itertools.count()
class TOK(enum.Enum):
    """
    Command Parser Tokens.
    """
    UNKNOWN                     = next(iota)
    VERB                        = next(iota)
    NOUN                        = next(iota)
    ADJ                         = next(iota)
    SUP                         = next(iota)
    OF                          = next(iota)
    PHRASAL                     = next(iota)
    PREP                        = next(iota)
    INDEF                       = next(iota)
    SPEC                        = next(iota)
    QUANT                       = next(iota)
    ORD                         = next(iota)
    COMMA                       = next(iota)
    AND                         = next(iota)
    STRING                      = next(iota)
    END                         = next(iota)


