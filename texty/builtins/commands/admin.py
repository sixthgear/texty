from texty.engine.command import command, syntax, parser
from texty.engine.story import Story

import importlib
import imp
import types


@command ("reset")
def reset(command, verb, object, prep, complement):
    if not command.source.is_a('admin'):
        return
    Story.get().clean()


@command ("reload")
def reload(command, verb, object, prep, complement):

    if not command.source.is_a('admin'):
        return

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
        command.response(module.__name__)

    # command.response('commands: %d' % len(parser.command_table))

    command.response('Reloading texty...')
    rr(importlib.import_module('texty.builtins'))

    command.response('commands: %d' % len(parser.command_table))
    command.response('objects: %d' % len(parser.object_table))
    # TODO: recreate existing objects
    return command.response('Done.')


# @command ("broadcast")
# def reload(command, verb, object, prep, complement, string):

#     if not command.source.is_a('admin'):
#         return


