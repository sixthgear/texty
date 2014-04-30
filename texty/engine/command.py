from texty.util.exceptions import TextyException
from texty.engine import obj
from texty.engine.parser import parser
from texty.util.parsertools import VOCAB
from texty.util.enums import SCOPE

from pprint import pprint
import traceback
import logging
import re


class ObjectASTProxy(object):
    """
    Proxy Object that allows commands to refer to the same object both before resolution (when it
    a set of descriptions from the AST) and after is has been resolved into a real-world object.
    """
    def __init__(self, ast_node, command):
        self.command = command
        self.ast_node = ast_node
        self.scope = None
        self.container = None
        self.obj = None

    def provided(self):
        return self.ast_node != None

    def resolve(self, scope=SCOPE.ANY, target=None):
        if not self.ast_node:
            raise TextyException('No AST node provided for ObjectASTProxy.', str(self))
        if target:
            target = target.obj

        result = self.command.resolve(self.ast_node, scope=scope, target=target)

        self.obj = result[0]
        self.scope = result[1]
        self.container = result[2]

        return self.obj != None

    def is_resolved(self):
        if not self.obj:
            raise TextyException('AST node {} has not been resolved.', str(self))
        return True

    def is_a(self, what):
        self.is_resolved()
        return self.obj.is_a(what)

    def is_any(self, what):
        self.is_resolved()
        return self.obj.is_any(what)

    def allows(self, what):
        self.is_resolved()
        return self.obj.allows(what)

    def __str__(self):

        if self.obj:
            return self.obj.name
        elif self.ast_node:
            desc = {}
            desc['detr'] = 'a' # {indef}{spec} {quant}{ord}'.format(**self.ast_node),
            desc['terms'] = str.join(', ', self.ast_node.get('terms'))
            if isinstance(self.ast_node.get('noun'), str):
                desc['noun'] = self.ast_node.get('noun')
            else:
                desc['noun'] = str.join(' ', self.ast_node.get('noun'))
            return '{detr} {terms} {noun}'.format(**desc)
        else:
            return ''


class Command(object):
    """
    Command objects are passed to each command function. They serve to provide a point of
    reference to the command function about the source of the command and other important aspects
    of the game state.

    TODO: this should give a reference to the Map object somehow.
    """

    UNKNOWN = "You aren't sure how to {verb}."

    def __init__(self, source, command, room=None, echo=True):
        self.source = source
        self.command = command
        self.room = room or source.room
        self.should_echo = echo
        self.do_next = []

    def parse(self):
        self.fn, self.ast = parser.parse(self.command)
        # pprint(self.ast)

    def run(self):
        """
        Execute the command.
        """
        # parse command
        # save reference to ast to use in helper funcions
        if not self.fn and self.ast:
            self.parse()

        # echo command to terminal
        self.echo()

        # no callable returned by parser
        if not self.fn:
            if self.ast:
                self.response(self.UNKNOWN.format(**self.ast))
            return

        # TODO: perform noun preresolution from syntax table
        # execute the callable
        try:
            response = self.fn(self, **self.ast) or None
        except TextyException as e:
            return self.response(e.message)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            return self.response('You broke something, jerk.')

        # flush the do_next queue and execute commands
        for command in self.do_next:
            self.source.do(command)

    def echo(self):
        """
        Echo the command back to the client
        """
        if self.should_echo:
            echo = self.command
            self.source.send({'type': 'command', 'command': echo})

    def response(self, message):
        """
        Send the response to the echo
        """

        logging.info('%s: %s' % (self.source.name, message))
        logging.info('---')
        if self.should_echo:
            self.source.send({'type': 'command', 'response': message})

    def enqueue(self, command):
        """
        Enqueue follow-up commands to execute next.
        TODO: these should perhaps be scheduled to respect tick fairness.
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

    def rules(self, *rules):
        """
        Apply dem rules.
        """
        # make proxy objects to pass back and forth
        x = ObjectASTProxy(self.ast.get('object'), command=self)
        y = ObjectASTProxy(self.ast.get('complement'), command=self)

        # iterate rules
        message = None
        for rule, m in rules:
            # rule failed
            out = rule(x, y)
            message = m.format(x=str(x), y=str(y), R=out)
            if not out:
                raise TextyException(message)

        # send out final message as a response,
        # then yield control back to command function with resolved objects
        return True, message, x, y


    def resolve(self, node, scope=SCOPE.ANY, attr=None, target=None):
        """
        Given a node from the AST and optional scope paramaters, resolve the token
        into an actual object.
        """

        compound_scopes = {
            SCOPE.HAS:      [SCOPE.EQUIP, SCOPE.INV, SCOPE.BODY],
            SCOPE.ROOM:     [SCOPE.OBJ, SCOPE.CHAR],
            SCOPE.ANY:      [SCOPE.EQUIP, SCOPE.INV, SCOPE.BODY, SCOPE.OBJ, SCOPE.CHAR],
        }

        if not target:
            target = self.source

        noun = node.get('noun')
        terms = node.get('terms')

        if scope in (SCOPE.ANY, SCOPE.ROOM, SCOPE.CHAR) and noun in ('self', 'me', 'myself'):
            return (self.source, scope, self.room)

        if scope in (SCOPE.ANY, SCOPE.ROOM) and noun in ('floor', 'ground', 'room'):
            return (self.room, scope, self.room)
        # search each scope
        for s in (compound_scopes.get(scope) or [scope]):

            if s == SCOPE.IN:
                if target.is_a('room'):
                    source = target.objects
                else:
                    source = target.contents
            elif s == SCOPE.EQUIP:
                source = target.equipment
            elif s == SCOPE.INV:
                source = target.inventory
            elif s == SCOPE.BODY:
                source = target.body
            elif s == SCOPE.OBJ:
                source = self.room.objects
            elif s == SCOPE.CHAR:
                source = self.room.characters
            else:
                source = None

            result = source.first(noun, terms=terms, attribute=attr)

            # return the resolved object and the scope it was found in
            if result:
                return (result, s, source)

        return (None, scope, None)


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



def admin(fn):
    """
    A decorator for supplying admin command definitions and aliases
    """
    # nonlocal x = 0

    def decorator(cmd, *args, **kwargs):


        # print('calling', cmd, kwargs)

        if not cmd.source.is_a('admin'):
            raise TextyException(Command.UNKNOWN.format(**kwargs))

        return fn(cmd, *args, **kwargs)

    return decorator


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
