# scopes = {'E': 'eq','I': 'inv','MY': 'my','R': 'room',}
ignores =       set(('a','an','the','of'))
prepositions =  set(('at','with','from','to','in','out','on','into'))
counters =      set(('all', 'each', 'every', 'everything'))
ordinals = {
    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5,
    'sixth': 6,
    'seventh': 7,
    'eighth': 8,
    'nineth': 9,
    'ninth': 9,
    'tenth': 10,
    '1st': 1,
    '2nd': 2,
    '3rd': 3,
    '4th': 4,
    '5th': 5,
    '6th': 6,
    '7th': 7,
    '8th': 8,
    '9th': 9,
    '10th': 10,
}
special_adjectives = {
    'my': None,   # limit scope to player equipment and inventory
    'last': None, # set the ordinal to the maximum
    'best': None,
    'worst': None
}

# ------------------------------------------------

class Atom(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        v = self.value
        return v

class Noun(Atom):
    def __init__(self, value, ordinal=1, number=1, scope=None):
        super(Noun, self).__init__(value=value)
        self.ordinal = ordinal
        self.number = number
        self.scope = scope
        self.results = []

    def __repr__(self):
        v = self.value
        if self.scope: v = '%s:%s' % (self.scope, self.value)
        if self.ordinal > 1: v = '%d.%s' % (self.ordinal, v)
        elif self.number > 1: v = '%d %s' % (self.number, v)
        return v

class List(Noun):
    pass

class Verb(Atom):
    def __init__(self, value):
        super(Verb, self).__init__(value=value)
        # self.fn = fn

class Prep(Atom):
    def __init__(self, value, optional=False):
        super(Prep, self).__init__(value=value)
        self.optional = optional

    def __repr__(self):
        v = self.value
        if self.optional: v = '[%s]' % v
        return v
