"""
Information commands.
"""
from texty.builtins.commands.movement import DIRECTIONS
from texty.engine.command import syntax, alias
import random


@syntax  ("look")
@syntax  ("look [at] OBJECT")
@syntax  ("look in CONTAINER")
@alias   ("examine")
def look(command):
    """
    LOOK -- give a description of places, people or objects

    look
    look [at] room

        show the description of the current room.

    look [at] [my]self
    look [at] me

        show the description of your character.

    look [at] <character>

        show the description of the named character in the room.

    look [at] <object>

        show the description of the named object in the room, or
        the player's inventory.

    look [at] <direction>

        show the description of the room in the given direction.

    look in[side] <object>

        display the contents of the named object in the room or
        the player's inventory.
    """
    look_in = False
    look_my = False
    object = None

    if len(command.arguments) == 0:
        object = command.room

    for a in list(command.arguments):
        # loop through arguments
        if a in ('in', 'inside'):
            # switch to "in" mode, and keep searching
            look_in = True
            continue
        elif a in ('my'):
            look_my = True
            continue
        elif a in ('room', 'around', 'area'):
            # room is a special name to refer to the current room
            object = command.room
            break
        elif a in ('me', 'self', 'myself'):
            # me|self|myself is a special name to refer to player
            object = command.source
            break
        else:
            # no special words found, begin searching objects
            if look_my:
                object = command.source.inventory.search_one(a) or None
                if not object:
                    return 'You don\'t seem to have that.'
            else:
                object = \
                    command.room.characters.search_one(a) or \
                    command.room.objects.search_one(a) or \
                    command.source.inventory.search_one(a) or \
                    command.room.exits[a] or None
                break

    if object:
        if look_in:
            # check if object is a container
            try:
                contents = object.contents
            except AttributeError:
                return command.response('You can\'t look inside that!')

            command.response('You examine the contents of %s.' % object.name)

            if len(contents):
                # return a list of the contents
                objs = {'type': 'object', 'items': [o.serialize() for o in contents]}

            else:
                objs = {'type': 'object', 'items': [{'text': 'Nothing.'}]}

            command.to_source(objs)
            return


        elif object == command.room:

            room = {
                'type': 'description',
                'intro': object.title,
                'text': object.description,
            }

            chars = [c.serialize() for c in object.characters if c != command.source]
            objs = [o.serialize() for o in object.objects]
            things = {'type': 'object', 'items': chars+objs}

            command.response('You examine your surroundings.')
            command.to_source(room)
            command.to_source(things)
            return

        else:
            # return the description of the object
            command.response('You examine %s.' % object.name)
            command.to_source(object.description)
            return
    else:
        return command.response('You don\'t see that here.')

@syntax ("inventory")
def inventory(command):
    d = 'You are carrying:\n'
    if not command.source.inventory:
        d += '    Nothing.\n'
    for o in command.source.inventory:
        d += '    %s\n' % o.name
    d += '\n'
    command.to_source(d)
    return

@syntax ("equipment")
def equipment(command):
    d = 'You are equiping:\n'
    if not command.source.equipment:
        d += '    Nothing.\n'
    for o in command.source.equipment:
        d += '    %s\n' % o.name
    d += '\n'
    command.to_source(d)
    return
