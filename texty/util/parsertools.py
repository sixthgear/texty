vocab = lambda v: set([x.strip() for x in v.split('|')])
class VOCAB:
    prepositions = vocab('at | in | inside | out | outside | into | on | to | upon | with | from | using')
    indefinites = vocab('a | an | any')
    specifics = vocab('my | the')
    quantifiers  = vocab('1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10')
    quantifiers |= vocab('one | two | three | fouth | five | six | seven | eight | nine | ten ')
    quantifiers |= vocab('all | both | each | every | everything')
    ordinals  = vocab('first | second | third | fourth | fifth | sixth | seventh | eighth | nineth | ninth | tenth | last')
    ordinals |= vocab('1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th')
    superlatives = vocab('best | worst | closest | furthest | biggest | largest | smallest | dumbest')

class TOK(object):
    """
    Data type for a processed symbol from the command.
    """
    UNKNOWN,  VERB,  NOUN,  ADJ,  SUP,  OF,  PREP,  INDEF, SPEC,  QUANT, ORD,  COMMA,  AND,  END = range(14)

    DESC = {
        UNKNOWN:    'UNKNOWN',
        VERB:       'VERB',
        NOUN:       'NOUN',
        ADJ:        'ADJ',
        SUP:        'SUP',
        OF:         'OF',
        PREP:       'PREP',
        INDEF:      'INDEF',
        SPEC:       'SPEC',
        QUANT:      'QUANT',
        ORD:        'ORD',
        COMMA:      'COMMA',
        AND:        'AND',
        END:        'END',
    }

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __repr__(self):
        if self.val:
            return '%s: "%s"' % (self.DESC.get(self.typ), self.val)
        else:
            return '%s' % (self.DESC.get(self.typ))

