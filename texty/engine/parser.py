from texty.util import commandlist
from texty.util import parsertools

import collections
import itertools


class Parser(object):
    """
    This object is responsible for taking player input and turning it into a
    function call for a command. Returns a command object.
    """

    OOPS = [
        'You don\'t know how to "%s".',
    ]

    def __init__(self):

        self.syntax_table = commandlist.SyntaxTable()
        self.command_table = collections.OrderedDict()
        self.object_table = []
        self.keyword_table = set()
        self.attribute_table = set()

    def register_syntax(self, syntax):
        """
        Register a syntax in the command table.
        Stories can use this to add custom commands to the dictionary.
        The syntax decorator in engine.parsertools will call this function automatically when
        defining a command definition.
        """
        self.syntax_table.append(syntax)

    def register_command(self, fn):
        """
        Register a command in the command table
        """
        self.command_table[fn.__name__] = fn

    def register_object(self, obj):
        """
        Register an object in the object table.
        """
        self.object_table.append(obj)
        self.keyword_table.update(obj.keywords)
        self.attribute_table.update(obj.attributes)


    def parse(self, command, source):
        """
        Parse the effer.
        """
        # lex the command
        tokens = command.split()

        # remove ignorned tokens
        # tokens = [t for t in tokens if t not in parsertools.ignores]
        if len(tokens) == 0:
            return None, []

        verb = tokens[0].lower()

        for t in tokens:
            tag = ''
            if t in self.command_table:
                tag += 'V'
            if t in self.keyword_table:
                tag += 'N'
            if t in parsertools.ordinals:
                tag += 'ORD'
            if t in parsertools.prepositions:
                tag += 'P'
            if not tag:
                tag = '?'

        commands = [c for c in self.command_table if c.startswith(verb)]
        if commands:
            return self.command_table[commands[0]], []

        # could not find any verb to match that command
        return self.error, [verb]

    def error(self, command):
        """
        this method is called if the interpreter doesn't understand the player input at all.
        """
        verb = command.arguments[0]
        return command.response(self.OOPS[0] % verb)


# global parser object
parser = Parser()
