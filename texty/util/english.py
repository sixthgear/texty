"""
Helper functions to make nice english output.
"""
import enum

class STR:

    class INFO:
        # activity        = "<b>{x.display}</b> {x.occupation} {are} {x.activity} here."
        here            = "<b>{sub.display}</b> {are} here."
        inside          = "<b>{sub.display}</b> {are} inside."
        wearing         = "{He} {is} wearing <b>{x.name}</b> on {his} {y}."
        holding         = "{He} {is} holding <b>{x.name}</b> in {his} {y}."
        inv             = "{He} {has} {x}."

    class SENSE:
        sense_near      = "You {sense} {x} nearby!"
        sense_far       = "You {sense} {x} in the distance."

    class STAT:
        slow            = "You feel sluggish."
        cold            = "You feel cold."
        dizzy           = "You feel lightheaded."
        hungry          = "You feel hungry."
        heart           = "Your heart is pounding."
        ring            = "Your ears are ringing."
        blind           = "You can't see."
        bleed_A         = "{He} {is} bleeding."
        bleed_B         = "{He} {is} bleeding profusely from several wounds."
        bleed_pt_A      = "{His} {head} {is} bleeding."
        bleed_pt_B      = "{His} {head} {is} severely bleeding."
        sick            = "{He} {is} coughing."
        breath          = "{He} {is} gasping for breath."
        blind           = "{He} stumble{s} around blindly."
        shock           = "{He} {is} in shock."
        uncons          = "{He} {is} unconscious."
        dead            = "{He} {has} died."

    class MOVE:
        leave           = "{Name} head{s} to {room.name} {direction}."
        arrive          = "{Name} arrive{s} from {room.name} {direction}."
        enter           = "{Name} enter{s} {room.name}."
        exit            = "{Name} leave{s} {room.name}."
        flee            = "{Name} retreat{s} {direction} to {room.name}"

    class FIGHT:
        ammo            = "{You} {have} {amount} {rounds} remaining in {your} {weapon}."
        empty           = "{Your} {weapon} is now empty."
        ready           = "{Name} read{ies} {his} {weapon}."
        relax           = "{Name} relax{es} {his} {weapon}."
        aim             = "{Name} point{s} {his} {weapon} at {you} to {direction}."
        fire_A          = "{Name} fire{s} {amount} {rounds} from {his} {weapon}."
        fire_B          = "{Name} take{s} aim and fire{s} {amount} {rounds} from {his} {weapon} at {you}."
        fire_C          = "{Name} unleash{es} a hail of automatic gunfire!"
        swing_A         = "{Name} swing{s} {his} {weapon} mercilessly at {you}."
        swing_B         = ""
        stab_A          = ""
        stab_B          = ""
        hit_pt_A        = "{Name} {is} {shot} in the {head}."
        hit_pt_B        = "{Name} take{s} {num} {shots} to the {head}."
        crit_A          = "{Names} skull crumples under the weight of {your} powerful blow!"
        crit_B          = "{Name} {is} shot cleanly between the eyes!"
        crit_C          = "{Name} {is} cut to ribbons by {your} accurate firing! {Its} remaining body parts spill across the {ground}."
        crit_D          = "{Names} slice neatly severs {your} head from {your} shoulders!"
        stun            = "{Name} {is} stunned for a moment, but continues to {approach} {you}!"
        death           = "{Name} crumple{s} to the ground gurgling and convulsing."


    @classmethod
    def T(cls, string, subject, object=None, source=None, extra=None):
        """
        """
        if not extra:
            extra = {}

        if source == subject:
            gender = 'Y'
        else:
            gender = subject.gender

        trans = {
            # name
            'name':                 PN.sub('Y') if gender == 'Y' else subject.name,
            'names':                PN.pos('Y') if gender == 'Y' else subject.name + "'s",
            'Name':                 PN.sub('Y').title() if gender == 'Y' else subject.name,
            'Names':                PN.pos('Y').title() if gender == 'Y' else subject.name + "'s",
            # subjective
            'You':                  PN.sub(gender).title(),
            'you':                  PN.sub(gender),
            'He':                   PN.sub(gender).title(),
            'he':                   PN.sub(gender),
            # objective
            'him':                  PN.obj(gender),
            # possesive
            'Your':                 PN.pos(gender).title(),
            'your':                 PN.pos(gender),
            'His':                  PN.pos(gender).title(),
            'his':                  PN.pos(gender),
            'Its':                  PN.pos(gender).title(),
            'its':                  PN.pos(gender),
            # reflexive
            'hisself':              PN.ref(gender),
            'yourself':             PN.ref(gender),
            # auxillary verbs
            's':                    PN.plural_s(gender),
            'es':                   PN.plural_es(gender),
            'ies':                  PN.plural_ies(gender),
            'is':                   PN.are(gender),
            'are':                  PN.are(gender),
            'has':                  PN.have(gender),
            'have':                 PN.have(gender),
            'isnt':                 PN.arent(gender),
            'arent':                PN.arent(gender)
        }
        trans.update(extra)

        return string.format(sub=subject, obj=object, **trans)

def resolve_single(subject, string, source=None):
    return STR.T(string, subject=subject, source=source)

class PN:
    """
    Pronoun table to use in action descriptions.
    """
    class TYPES(enum.Enum):
        """
        Types of pronouns.
        """
        SUB = 0
        OBJ = 1
        POS = 2
        REF = 3

    MAP = {
        #       | SUB  | OBJ   | POS   | REF            # PRO
        # ----------------------------------------------#------------
        'Y':    ['you', 'you',  'your', 'yourself'],    # 'yours',
        'M':    ['he',  'him',  'his',  'hisself'],     # 'his',
        'F':    ['she', 'her',  'her',  'herself'],     # 'hers',
        'N':    ['it',  'it',   'its',  'itself'],      # 'its',
        'G':    ['they' 'them', 'their','themself'],    # 'theirs',
    }

    @classmethod
    def sub(cls, gender):
        return cls.MAP[gender][cls.TYPES.SUB.value]

    @classmethod
    def obj(cls, gender):
        return cls.MAP[gender][cls.TYPES.OBJ.value]

    @classmethod
    def pos(cls, gender):
        return cls.MAP[gender][cls.TYPES.POS.value]

    @classmethod
    def ref(cls, gender):
        return cls.MAP[gender][cls.TYPES.REF.value]

    @classmethod
    def arent(cls, gender):
        return 'aren\'t' if gender == 'Y' else 'isn\'t'

    @classmethod
    def have(cls, gender):
        return 'have' if gender == 'Y' else 'has'

    @classmethod
    def are(cls, gender):
        return 'are' if gender == 'Y' else 'is'

    @classmethod
    def plural_ies(cls, gender):
        return 's' if gender == 'Y' else 'ies'

    @classmethod
    def plural_es(cls, gender):
        return '' if gender == 'Y' else 'es'

    @classmethod
    def plural_s(cls, gender):
        return '' if gender == 'Y' else 's'
