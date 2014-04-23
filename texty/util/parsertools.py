from texty.util.enums import TOK

v = lambda x: set([x.strip() for x in x.split('|')])

class VOCAB:
    """
    Dictionary of accepted symbols.
    """
    # special set that is updated as players enter or leave the game
    characters      =   set()

    # filled in dyamically
    commands        =   v('say | yell | shout | tell')
    verbs           =   set()
    nouns           =   set()
    adjectives      =   set()
    phrasals        =   set() # v('at | up | down | away | on | off ')

    # set of reserved nouns
    reserved        =   v('me | room | myself | self | floor | ground')

    superlatives    =   v('best | worst | closest | furthest | biggest | largest | smallest | dumbest')

    prepositions    =   v('above | against | ahead | around | at | behind | below')
    prepositions   |=   v('for | from | in | inside | into | off | on | out | outside | over')
    prepositions   |=   v('through | to | toward | under | upon | using | with')

    indefinites     =   v('a | an | any')
    specifics       =   v('my | the')

    quantifiers     =   v('1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10')
    quantifiers    |=   v('one | two | three | fouth | five | six | seven | eight | nine | ten ')
    quantifiers    |=   v('all | both | each | every | everything')

    ordinals        =   v('first | second | third | fourth | fifth | sixth')
    ordinals       |=   v('seventh | eighth | nineth | ninth | tenth | last')
    ordinals       |=   v('1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th')

    tranformations = {
        'my self':      'myself'
    }


class Token(object):
    """
    Data type for a processed symbol from the command.
    """

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __repr__(self):
        if self.val:
            return '%s: "%s"' % (self.typ, self.val)
        else:
            return self.typ
