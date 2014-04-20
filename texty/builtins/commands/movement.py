"""
Movement commands.
"""
from texty.engine.command import command, syntax

DIRECTIONS = {
    'north':    'north',
    'east':     'east',
    'south':    'south',
    'west':     'west',
    'up':       'up',
    'down':     'down'
}

OPPOSITES = {
    'north':    'to the south',
    'east':     'to the west',
    'south':    'to the north',
    'west':     'to the east',
    'up':       'below',
    'down':     'above'
}

# @command ("go [to] EXIT")
@command ("go", "walk")
def go(command, verb, object, prep, complement):

    if len(command.arguments) == 0:
        return command.response('Go where?')
    try:
        direction = DIRECTIONS[command.arguments[0]]
    except KeyError:
        return command.response('What direction is that?!?')

    if command.room.exits.has_key(direction):

        old_room = command.source.room
        new_room = command.room.exits[direction]

        room_to = '<b>%s</b> to <b>%s</b>' % (direction, new_room.title)
        room_from = '<b>%s</b> <b>%s</b>' % (old_room.title, OPPOSITES[direction])

        command.response('You head %s.' % room_to)
        command.to_room('A: <b>%s</b> heads %s.' % (command.source.name, room_to))

        command.source.move_to(new_room)

        # send message to new room
        new_room.send(
            'A: <b>%s</b> arrives from %s.' % (command.source.name, room_from),
            source=command.source)

        command.enqueue('look')
        return

    else:
        return command.response('Can\'t go that way.')

@command ("north", "n")
def north(command, verb, object, prep, complement):
    command.arguments = ['north']
    return go(command, verb, object, prep, complement)

@command ("south", "s")
def south(command, verb, object, prep, complement):
    command.arguments = ['south']
    return go(command, verb, object, prep, complement)

@command ("east", "e")
def east(command, verb, object, prep, complement):
    command.arguments = ['east']
    return go(command, verb, object, prep, complement)

@command ("west", "w")
def west(command, verb, object, prep, complement):
    command.arguments = ['west']
    return go(command, verb, object, prep, complement)

@command ("up", "u")
def up(command, verb, object, prep, complement):
    command.arguments = ['up']
    return go(command, verb, object, prep, complement)

@command ("down", "d")
def down(command, verb, object, prep, complement):
    command.arguments = ['down']
    return go(command, verb, object, prep, complement)

@command ("enter")
def enter(command, verb, object, prep, complement):
    return None

@command ("exit")
def exit(command, verb, object, prep, complement):
    return None
