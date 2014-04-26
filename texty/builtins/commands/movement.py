"""
Movement commands.
"""
from texty.engine.command import command, syntax
from texty.util.enums import DIRECTIONS

opposites = {
    DIRECTIONS.NORTH:    'to the south',
    DIRECTIONS.EAST:     'to the west',
    DIRECTIONS.SOUTH:    'to the north',
    DIRECTIONS.WEST:     'to the east',
    DIRECTIONS.UP:       'below',
    DIRECTIONS.DOWN:     'above'
}

@command ("go", "walk")
def go(command, verb, object, prep, complement):

    if not object:
        return command.response('Go where?')

    if object.lower().startswith('n'):
        direction = DIRECTIONS.NORTH
    elif object.lower().startswith('s'):
        direction = DIRECTIONS.SOUTH
    elif object.lower().startswith('e'):
        direction = DIRECTIONS.EAST
    elif object.lower().startswith('w'):
        direction = DIRECTIONS.WEST
    elif object.lower().startswith('u'):
        direction = DIRECTIONS.UP
    elif object.lower().startswith('d'):
        direction = DIRECTIONS.DOWN
    else:
        return command.response('What direction is that?!?')

    if direction not in command.room.exits:
        return command.response('Can\'t go that way.')
    else:
        old_room = command.source.room
        new_room = command.room.exits[direction]
        room_to = '<b>%s</b> to <b>%s</b>' % (direction.name.lower(), new_room.name)
        room_from = '<b>%s</b> <b>%s</b>' % (old_room.name, opposites[direction])
        command.response('You head %s.' % room_to)
        command.to_room('MV: <b>%s</b> heads %s.' % (command.source.name, room_to))
        command.source.move_to(new_room)
        # send message to new room
        new_room.send(
            'MV: <b>%s</b> arrives from %s.' % (command.source.name, room_from),
            source=command.source)
        command.enqueue('look')
        return


@command ("north", "n", "go north", "walk north")
def north(command, verb, object, prep, complement):
    return go(command, 'go', 'north', prep, complement)

@command ("south", "s", "go south", "walk south")
def south(command, verb, object, prep, complement):
    return go(command, 'go', 'south', prep, complement)

@command ("east", "e", "go east", "walk east")
def east(command, verb, object, prep, complement):
    return go(command, 'go', 'east', prep, complement)

@command ("west", "w", "go west", "walk west")
def west(command, verb, object, prep, complement):
    return go(command, 'go', 'west', prep, complement)

@command ("up", "u", "go up", "walk up", "climb", "climb up")
def up(command, verb, object, prep, complement):
    return go(command, 'go', 'up', prep, complement)

@command ("down", "d", "go down", "climb down")
def down(command, verb, object, prep, complement):
    return go(command, 'go', 'down', prep, complement)

@command ("enter")
def enter(command, verb, object, prep, complement):
    return None

@command ("exit", "leave", "go out")
def exit(command, verb, object, prep, complement):
    return None
