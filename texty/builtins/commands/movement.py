"""
Movement commands.
"""

from texty.engine.command import syntax, alias
from texty.util.searchdict import SearchDict

DIRECTIONS = SearchDict({
    'north': 'north',
    'east': 'east',
    'south': 'south',
    'west': 'west',
    'up': 'up',
    'down': 'down'
}, quiet=False)

OPPOSITES = {
    'north': 'to the south',
    'east': 'to the west',
    'south': 'to the north',
    'west': 'to the east',
    'up': 'below',
    'down': 'above'
}

@syntax ("go [to] EXIT")
def go(command):

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

@syntax ("north")
def north(command):
    command.arguments = ['north']
    return go(command)

@syntax ("south")
def south(command):
    command.arguments = ['south']
    return go(command)

@syntax ("east")
def east(command):
    command.arguments = ['east']
    return go(command)

@syntax ("west")
def west(command):
    command.arguments = ['west']
    return go(command)

@syntax ("up")
def up(command):
    command.arguments = ['up']
    return go(command)

@syntax ("down")
def down(command):
    command.arguments = ['down']
    return go(command)

@syntax ("enter ENTERABLE")
def enter(command):
    return None

@syntax ("exit ENTERABLE")
def exit(command):
    return None
