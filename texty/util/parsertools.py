
class VOCAB:

    v = lambda v: set([x.strip() for x in v.split('|')])

    # special set that is updated as players enter or leave the game
    characters      =   set()

    # filled in dyamically
    nouns           =   set()
    adjectives      =   set()
    superlatives    =   v('best | worst | closest | furthest | biggest | largest | smallest | dumbest')

    prepositions    =   v('above | against | ahead | around | at | away | back | behind | below')
    prepositions   |=   v('down | for | from | in | inside | into | off | on | out | outside | over')
    prepositions   |=   v('through | to | toward | under | up | upon | using | with')

    indefinites     =   v('a | an | any')
    specifics       =   v('my | the')

    quantifiers     =   v('1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10')
    quantifiers    |=   v('one | two | three | fouth | five | six | seven | eight | nine | ten ')
    quantifiers    |=   v('all | both | each | every | everything')

    ordinals        =   v('first | second | third | fourth | fifth | sixth')
    ordinals       |=   v('seventh | eighth | nineth | ninth | tenth | last')
    ordinals       |=   v('1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th')


class TOK(object):
    """
    Data type for a processed symbol from the command.
    """
    UNKNOWN, VERB, NOUN, ADJ, SUP, OF, PREP, INDEF, SPEC, QUANT, ORD, COMMA, AND, END = range(14)

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

