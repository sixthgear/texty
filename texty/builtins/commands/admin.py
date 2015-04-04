from texty.builtins.characters.player import Player
from texty.engine.command import command, admin, syntax, parser, Command
from texty.engine.story import Story
from texty.util import serialize
from texty.util.exceptions import TextyException
from texty.util.english import STR

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
        return cmd.response(STR.ERROR.unknown.format(verb=verb))

@command ("break")
def _break(cmd, verb, object, prep, complement, string=None):
    """
    """
    cmd.response('Breaking...')
    import pdb; pdb.set_trace()

@command ("unadmin")
@admin
def unadmin(cmd, verb, object, prep, complement, string=None):
    """
    """
    cmd.source.attributes.remove('admin')
    return cmd.response('Done.')


@command ("reset")
@admin
def reload(cmd, verb, object, prep, complement):
    """
    """
    cmd.response('Reloading texty...')
    cmd.response('Resetting story...')

    players = Story.get().get_players()
    storyname = Story.get().loaded_storyname
    story = Story.load(storyname)

    for p in players:
        p.send('A:Game is resetting.')
        p.__init__(p.name, connection=p.connection)
        story.on_player_connect(p)

    return cmd.response('Done.')


# @admin ("broadcast")
# def reload(command, verb, object, prep, complement, string):

#     if not command.source.is_a('admin'):
#         return

@command ("warp", "goto")
@admin
def warp(cmd, verb, object, prep, complement, string=None):


    if not string:
        raise TextyException("Warp where?")

    m = Story.get().map
    node = m.nodes.get(string.upper())
    if not node:
        raise TextyException("Node ID {} not found.".format(string))

    cmd.source.move_to(node)
    cmd.enqueue('look')
    return cmd.response('You warp to {}.'.format(node))
    # room = cmd.

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


