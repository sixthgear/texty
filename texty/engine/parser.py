from texty.util.exceptions import ParserError
from texty.util.parsertools import Token, VOCAB, lookahead
from texty.util.enums import TOK
from texty.util.objectlist import ObjectList
import traceback
import logging
import collections
import re

class Parser(object):

    """
    This object is responsible for taking player input and turning it into a
    function call for a command. Returns a command object and a list of arguments
    to pass to the function.
    """

    def __init__(self):
        """
        Create lookup tables used to help parse commands and resolve nouns
        into their correct scopes.
        """
        # the command table is a dictionary mapping from a command name string to
        # the actual command function.
        self.command_table = collections.OrderedDict()
        # the syntax table is a list of language atoms used to map a phrase to
        # a command eg: (Verb, Noun, Prep, Noun) or (load WEAPON with AMMO)
        self.syntax_table = list()
        # the object table is a simple list of all objects registered in the game.
        self.object_table = ObjectList()
        self.attribute_table = set()

    def register_command(self, fn, name=None):
        """
        Register a command in the command table.
        """
        name = name or fn.__name__
        words = name.lower().split()
        if len(words) == 1:
            VOCAB.verbs.add(words[0])
        elif len(words) == 2:
            VOCAB.verbs.add(words[0])
            VOCAB.phrasals.add(words[1])
        else:
            raise ParserError('Commands must be one or two words.')
        self.command_table[name.lower()] = fn

    def register_syntax(self, syntax):
        """
        Register a syntax in the command table.
        Stories can use this to add custom commands to the dictionary.
        The syntax decorator in engine.parsertools will call this function automatically when
        defining a command definition.
        """
        self.syntax_table.append(syntax)

    def register_object(self, obj):
        """
        Register an object in the object table, and place its keywords and atrributes
        into their respective sets.
        """
        self.attribute_table.update(obj.attributes)
        VOCAB.nouns.update(obj.nouns)
        VOCAB.adjectives.update(obj.adjectives)

        self.object_table.append(obj)


    def lex(self, command):
        """
        Split a raw string into tokens and tag them with the class they belong to.
        The parser will use the stream of tokens from lex to determine semantics.
        """
        tokens = []

        class M:
            REGULAR             =   0
            VERB                =   1
            STRING              =   2


        mode = M.REGULAR



        # process each raw symbol in turn
        for t, next_t in lookahead(re.findall('\w+|[.,"]', command.lower())):

            # print (t, next_t)

            # check for an optional phrasal preposition or particle following a verb
            if mode == M.VERB:
                mode = M.REGULAR
                if t in VOCAB.phrasals:
                    tokens.append(Token(TOK.PHRASAL, t))
                    continue

            # the say command, among others, will accept a literal string of unparsed characters
            # so once we are in string mode, keep consuming string tokens until the end
            elif mode == M.STRING:
                if tokens[-1:] and tokens[-1].typ == TOK.STRING:
                    tokens[-1].val += ' %s' % t
                else:
                    tokens.append(Token(TOK.STRING, t))
                continue

            # regular mode
            if t == ',':
                tokens.append(Token(TOK.COMMA, t))
            elif t == 'of':
                tokens.append(Token(TOK.OF, t))
            elif t == '.':
                pass # ignore
                # tokens.append(Token(TOK.PERIOD, t))
            elif t == 'and':
                tokens.append(Token(TOK.AND, t))
            elif t in VOCAB.commands:
                tokens.append(Token(TOK.VERB, t))
                mode = M.STRING
            elif t in VOCAB.verbs:
                tokens.append(Token(TOK.VERB, t))
                mode = M.VERB
            elif t in VOCAB.prepositions:
                tokens.append(Token(TOK.PREP, t))
            elif t in VOCAB.indefinites:
                tokens.append(Token(TOK.INDEF, t))
            elif t in VOCAB.specifics:
                tokens.append(Token(TOK.SPEC, t))
            elif t in VOCAB.quantifiers:
                tokens.append(Token(TOK.QUANT, t))
            elif t in VOCAB.ordinals:
                tokens.append(Token(TOK.ORD, t))
            elif t in VOCAB.characters or t in VOCAB.reserved:
                tokens.append(Token(TOK.NOUN, t))
            # superlatives are special adjectives
            elif t in VOCAB.superlatives:
                tokens.append(Token(TOK.SUP, t))
            # ambiguous adjectives and nouns become a TERM
            elif t in VOCAB.adjectives or (t in VOCAB.adjectives and t in VOCAB.nouns):
                # transform last term into a noun for the parser
                if next_t and (next_t in VOCAB.adjectives | VOCAB.nouns):
                    tokens.append(Token(TOK.TERM, t))
                else:
                    tokens.append(Token(TOK.NOUN, t))

            # elif t in VOCAB.adjectives:
            #     tokens.append(Token(TOK.ADJ, t))

            elif t in VOCAB.nouns:
                tokens.append(Token(TOK.NOUN, t))

            elif t.endswith('s') and t[:-1] in VOCAB.nouns:
                tokens.append(Token(TOK.NOUN, t))

            else:
                tokens.append(Token(TOK.UNKNOWN, t))



        # append end token if it doesn't exist
        if tokens and tokens[-1].typ != TOK.END:
            tokens.append(Token(TOK.END, '.'))

        # return token stream
        # print (tokens)
        return tokens

    def parse(self, command):
        """
        Parse that fucker. Return an AST that can be used directly by commands.
        """
        # lex the command
        tokens = self.lex(command)

        if not tokens:
            return None, None

        # create token iterator
        iterator = iter(tokens)
        token = next(iterator, None)
        stack = []

        def accept(*rules):
            """
            Helper function to see if the token matches the given terminal or non-terminal,
            If yes, advance the token iterator if the argument was a terminal.
            """
            nonlocal token


            for rule in rules:

                if isinstance(rule, collections.Callable):
                    a, b = rule()
                    if a:
                        stack.append(b)
                        return True
                    # return a

                elif token.typ == rule:
                    stack.append(token.val)
                    token = next(iterator, None)
                    return True

            # none of the rules matched
            return False

        def expect(*rules):
            """
            Helper function to do the same thing as accept, but raise a ParserError if the
            match does not succeed.
            """
            nonlocal token

            if accept(*rules): # self.token and
                return True

            for rule in rules:
                if callable(rule):
                    raise ParserError('Expected %s, got %s.' % (rule.__name__.upper(), token))
                else:
                    raise ParserError('Expected %s, got %s.' % (rule.name, token))

        def parse_command():
            """
            Command ->  verb end
            Command ->  verb string end
            Command ->  verb prep NounPhrase end
            Command ->  verb NounPhrase end
            Command ->  verb NounPhrase prep NounPhrase end
            """
            cc = {
                'verb':                     None,
                'object':                   None,
                'prep':                     None,
                'complement':               None,
            }

            if expect(verb):
                cc['verb']                  = stack.pop()

                if accept(TOK.END):
                    return cc

                if accept(TOK.STRING) and expect(TOK.END):
                    _                       = stack.pop()
                    cc['string']            = stack.pop()
                    return cc

                if accept(TOK.PREP) and expect(nounphrase) and expect(TOK.END):
                    _                       = stack.pop()
                    cc['object']            = stack.pop()
                    cc['prep']              = stack.pop()
                    return cc

                if expect(nounphrase):
                    cc['object']            = stack.pop()

                    if accept(TOK.END):
                        return cc

                    if expect(TOK.PREP) and expect(nounphrase) and expect(TOK.END):
                        _                   = stack.pop()
                        cc['complement']    = stack.pop()
                        cc['prep']          = stack.pop()
                        return cc

        def verb():
            """
            Verb -> verb
            Verb -> verb phrasal
            """
            if accept(TOK.VERB):
                verb                        = stack.pop()

                if accept(TOK.PHRASAL):
                    verb             += ' ' + stack.pop()
                    return True, verb

                return True, verb

            return False, None


        def nounphrase():
            """
            NounPhrase -> Determiner TermList Noun
            NounPhrase -> Determiner Noun
            NounPhrase -> TermList Noun
            NounPhrase -> Noun
            """
            np = {
                'noun':                     None,
                'terms':                    [],
                'indef':                    None,
                'spec':                     None,
                'quant':                    None,
                'ord':                      None,
            }

            if accept(determiner):
                np.update(stack.pop())

                if accept(termlist) and expect(noun):
                    np['noun']              = stack.pop()
                    np['terms']             = stack.pop()
                    return True, np

                if expect(noun):
                    np['noun']              = stack.pop()
                    return True, np

            if accept(termlist) and expect(noun):
                np['noun']                  = stack.pop()
                np['terms']                 = stack.pop()
                return True, np

            if accept(noun):
                np['noun']                  = stack.pop()
                return True, np

            return False, None # not a nounphrase


        def noun():
            """
            Noun -> noun of noun
            Noun -> noun noun
            Noun -> noun
            # removed:
            ---- Noun -> noun noun ----
            """
            if accept(TOK.NOUN):
                n = stack.pop()

                if accept(TOK.NOUN):
                    return True, (n, stack.pop(),)

                if accept(TOK.OF) and expect(TOK.NOUN):
                    return True, (n, stack.pop(),)

                return True, n

            return False, None # not a noun

        def termlist():
            """
            TermList -> Term , TermList
            TermList -> Term TermList
            TermList -> Term
            """
            terms = []

            if accept(term):

                terms.append(stack.pop())

                if accept(TOK.COMMA) and expect(termlist):
                    return True, terms + stack.pop()

                if accept(termlist):
                    return True, terms + stack.pop()

                return True, terms

            return False, None # not an adjlist

        def term():
            """
            Term -> sup | sup of spec
            Term -> term
            Term -> adj
            """
            if accept(TOK.SUP):
                t = stack.pop()

                if accept(TOK.OF) and expect(TOK.SPEC):
                    return True, (t, stack.pop())

                return True, t

            if accept(TOK.TERM):
                return True, stack.pop()

            if accept(TOK.ADJ):
                return True, stack.pop()

            return False, None

        def determiner():
            """
            Determiner  ->  indef | spec | quant | ord
            Determiner  ->  spec ord | spec quant | quant spec
            Determiner  ->  ord of spec | quant of spec
            """
            d = {
                'indef': None,
                'spec': None,
                'quant': None,
                'ord': None,
            }

            if accept(TOK.INDEF):
                d['indef']                  = stack.pop()
                return True, d

            if accept(TOK.SPEC):
                d['spec']                   = stack.pop()

                if accept(TOK.ORD):
                    d['ord']                = stack.pop()
                    return True, d

                if accept(TOK.QUANT):
                    d['quant']              = stack.pop()
                    return True, d

                return True, d

            if accept(TOK.QUANT):
                d['quant']                  = stack.pop()

                if accept(TOK.SPEC):
                    d['spec']               = stack.pop()
                    return True, d

                if accept(TOK.OF) and expect(TOK.SPEC):
                    d['spec']               = stack.pop()
                    return True, d

                return True, d

            if accept(TOK.ORD):
                d['ord']                    = stack.pop()

                if accept(TOK.OF) and expect(TOK.SPEC):
                    d['spec']               = stack.pop()
                    return True, d

                return True, d

            return False, None


        command_ast = parse_command()
        return command_ast


    def error(self, command, message):
        """
        this method is called if the interpreter doesn't understand the player input at all.
        """
        return command.response(message)


# global parser object
parser = Parser()
