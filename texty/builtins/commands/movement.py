"""
Movement commands.
"""
from texty.engine.command import command, syntax
from texty.engine.node import DIR_ENG
from texty.util.enums import DIRECTIONS
from texty.util.english import STR

@command ("go", "walk")
def go(cmd, verb, object, prep, complement):

    if not object:
        return cmd.response('Go where?')

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
        return cmd.response('What direction is that?!?')

    if direction not in cmd.node.exits:
        return cmd.response('Can\'t go that way.')
    else:

        original = cmd.source.node
        target = cmd.node.exits[direction]


        cmd.node.move_dir(cmd.source, direction)

        extra = {
            'node': target,
            'direction': DIR_ENG[direction],
        }

        cmd.response(STR.T(STR.MOVE.leave, cmd.source, source=cmd.source, extra=extra))

        cmd.enqueue('look')

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
