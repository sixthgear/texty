from texty.engine.parser import parser
from texty.util.parsertools import Atom, Verb, Noun, List, Prep, prepositions
import re

class Command(object):
    """
    Command objects are passed to each command function to provide scope references
    """
    def __init__(self, source, command, room=None, status=1, echo=True):
        self.source = source
        self.room = room or source.room
        self.status = status
        self.callable, self.arguments = parser.parse(command, source)
        self.command = command
        self.should_echo = echo
        self.do_next = []

    def run(self):
        """
        Execute the command.
        """

        # send echo
        self.echo()

        if not self.callable:
            return None

        # execute the callable
        response = self.callable(self) or None

        # flush the do_next queue and execture commands
        for command in self.do_next:
            self.source.do(command)

    def echo(self):
        """
        Echo the command back to the client
        """
        if self.should_echo:
            if self.callable and self.callable.__name__ != 'error':
                echo = self.callable.__name__
            else:
                echo = self.command
            self.source.send({'type': 'command', 'command': echo})

    def response(self, message):
        """
        Send the response to the echo
        """
        if self.should_echo:
            self.source.send({'type': 'command', 'response': message})

    def enqueue(self, command):
        """
        Enqueue follow-up commands to execute next
        """
        self.do_next.append(command)

    def to_source(self, message):
        """
        Shortcut to send a message to the source character.
        """
        self.source.send(message)

    def to_room(self, message):
        """
        Shortcut to send a message to the source character's room.
        """
        room = self.room or self.source.room
        if not room:
            return
        room.send(message, source=self.source)


class syntax(object):
    """
    A decorator for supplying a command definition
    This adds the syntax into a table to help the parser know which command to call.
    """
    def __init__(self, syntax, aliases=[]):
        """
        parse the syntax into grammar atoms. This only happens once when server is started.
        """
        tokens = syntax.split()
        if not tokens: return
        self.atoms = [ Verb( tokens[0] ) ]

        for t in tokens[1:]:
            # optional checker
            t, optional = re.subn(r'\[(.*)\]$', r'\1', t, 1)
            optional = optional != 0

            # preposition list
            if t in prepositions:
                self.atoms.append( Prep(t, optional) )
                continue

            # noun checker
            m = re.match(r'([A-Z]+\.)?([A-Z]+)(\.\.\.)?$', t)
            if m:
                scope, attribute, multiple = m.groups()
                if scope: scope = scope[:-1]
                if multiple:
                    atom = List(attribute, 1, 1, scope)
                else:
                    atom = Noun(attribute, 1, 1, scope)

                self.atoms.append(atom)
                continue

        parser.register_syntax(self.atoms)

    def __call__(self, fn):
        """
        parse to command to perform automatic lookups
        """
        parser.register_command(fn)
        def wrapper(command):
            return fn(command)
        wrapper.__name__ = fn.__name__
        return wrapper


class alias(object):
    """
    A decorator for supplying an alias to an existing command definition
    """
    def __init__(self, *aliases):
        pass

    def __call__(self, fn):
        def wrapper(command):
            return fn(command)
        wrapper.__name__ = fn.__name__
        return wrapper
