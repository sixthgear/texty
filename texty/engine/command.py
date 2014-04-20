from texty.engine.parser import parser
# from texty.util.parsertools import Atom, Verb, Noun, List, Prep, prepositions
import re

class Command(object):
    """
    Command objects are passed to each command function to provide scope references
    """
    def __init__(self, source, command, room=None, status=1, echo=True):
        self.source = source
        self.command = command
        self.room = room or source.room
        self.status = status
        self.should_echo = echo
        # parse command
        self.callable, self.ast = parser.parse(command, source)
        self.do_next = []

    def run(self):
        """
        Execute the command.
        """
        self.echo()

        if not self.callable:
            return None
        # execute the callable

        # self.to_source(self.callable.__name__ + ' ' + str.join(' ', self.arguments))
        # return
        response = self.callable(self, **self.ast) or None
        # flush the do_next queue and execute commands
        for command in self.do_next:
            self.source.do(command)

    def echo(self):
        """
        Echo the command back to the client
        """
        if self.should_echo:
            # if self.callable and self.callable.__name__ != 'error':
            #     echo = self.callable.__name__
            # else:
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


    def reject(self, message):
        pass

    def resolve(self, node, scope='ALL', attribute=None, container=None):
        """
        Given a node from the AST and optional scope paramaters, resolve the token
        into an actual object.
        """

        compound_searches = {
            'MY':   ('E', 'I', 'B'),             # search source equipment and inventory and body
            'R':    ('C', 'O'),                  # search the room objects and characters
            'ALL':  ('E', 'I', 'B', 'O', 'C'),
        }

        searches = {
            'E':    self.source.equipment,
            'I':    self.source.inventory,
            'B':    self.source.body,
            'C':    self.room.characters,
            'O':    self.room.objects,
        }

        noun = node['noun']
        adjectives = node.get('adjl') or []
        ordinal = node.get('ord') or 1
        quantifier = node.get('quant') or 1

        if scope in compound_searches:
            scopes = compound_searches[scope]
        else:
            scopes = scope.split()

        for s in scopes:
            result = searches[s].first(
                query=noun,
                adjectives=adjectives,
                attribute=attribute,
            )
            if result:
                break

        return result


# DECORATORS FOR COMMAND FUNCTIONS
# --------------------------------

class command(object):
    """
    A decorator for supplying command definitions and aliases
    """
    def __init__(self, *aliases):
        self.aliases = aliases

    def __call__(self, fn):

        for a in self.aliases:
            parser.register_command(fn, name=a)

        def wrapper(command, *args, **kwargs):
            return fn(command, *args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper


class syntax(object):
    """
    A decorator for supplying a command definition
    This adds the syntax into a table to help the parser know which command to call.
    """
    def __init__(self, syntax, aliases=[]):
        """
        parse the syntax into grammar atoms. This only happens once when server is started.
        """
        pass

    def __call__(self, fn):
        """
        parse to command to perform automatic lookups
        """
        parser.register_command(fn)
        def wrapper(command, *args, **kwargs):
            return fn(command, *args, **kwargs)
        wrapper.__name__ = fn.__name__
        return wrapper
