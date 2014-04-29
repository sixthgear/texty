from texty.engine.command import command, admin, syntax, parser, Command
from texty.util.exceptions import TextyException
from texty.engine.story import Story
from texty.util import serialize

import importlib
import imp
import types

@command ("admin")
def _admin(cmd, verb, object, prep, complement, string=None):
    """
    """
    if string == '37773':
        cmd.source.attributes.add('admin')
        return cmd.response('Done.')
    else:
        return cmd.response(Command.UNKNOWN.format(verb=verb))


@command ("unadmin")
@admin
def unadmin(cmd, verb, object, prep, complement, string=None):
    """
    """
    cmd.source.attributes.remove('admin')
    return cmd.response('Done.')


@command ("reset")
@admin
def reset(cmd, verb, object, prep, complement):
    """
    """
    if not cmd.source.is_a('admin'):
        return
    Story.get().clean()


@command ("reload")
@admin
def reload(cmd, verb, object, prep, complement):
    """
    """
    done = set()
    def rr(module):
        if module in done or not module.__name__.startswith('texty.builtins'):
            return
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if type(attribute) is types.ModuleType:
                rr(attribute)
        imp.reload(module)
        done.add(module)
        cmd.response(module.__name__)

    # command.response('commands: %d' % len(parser.command_table))

    cmd.response('Reloading texty...')
    rr(importlib.import_module('texty.builtins'))

    cmd.response('commands: %d' % len(parser.command_table))
    cmd.response('objects: %d' % len(parser.object_table))
    # TODO: recreate existing objects
    return cmd.response('Done.')


# @admin ("broadcast")
# def reload(command, verb, object, prep, complement, string):

#     if not command.source.is_a('admin'):
#         return


@command ("create", "make", "mk")
@admin
def create(cmd, verb, object, prep, complement, string=None):
    """
    """

    if complement:
        raise TextyException("That doesn't make sense.")

    elif prep:
        raise TextyException("That doesn't make sense.")

    elif object:

        obj_class = parser.object_table.first(object['noun'], terms=object['terms'])

        if obj_class:
            obj = obj_class()
            cmd.source.inventory.append(obj)
            cmd.source.send(serialize.full_character(cmd.source))
            return cmd.response('You create {}.'.format(obj.name))
        else:
            return cmd.response('Not found.')

    elif verb:
        raise TextyException("Create what?")


