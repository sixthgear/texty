"""
Interaction commands.
"""
from texty.engine.command import syntax, alias

@syntax  ("get R.PORTABLE")
@syntax  ("get PORTABLE from CONTAINER")
@alias   ("pick up", "grab", "take")
def get(command):
    """
    Get an object from the room.
    """
    if len(command.arguments) == 0:
        return command.to_source('Get what?')
    if not command.arguments[0]:
        return command.to_source('You don\'t see that here.')
    for o in command.arguments[0]:
        if command.source.inv_weight + o.weight > command.source.capacity:
            return command.to_source('You are carrying too much to take that.')
        command.source.inventory.append(o)
        command.room.objects.remove(o)
        command.to_source('You take %s.' % o.name)
        command.to_room('%s takes %s.' % (command.source.name, o.name))

@syntax  ("drop I.PORTABLE")
@syntax  ("drop I.PORTABLE [on] FLOOR", "put, throw")
def drop(command):
    """
    Drop an object from inventory.
    """
    if len(command.arguments) == 0:
        return command.to_source('Drop what?')
    if not command.arguments[0]:
        return command.to_source('You don\'t have that.')
    for o in command.arguments[0]:
        command.room.objects.append(o)
        command.source.inventory.remove(o)
        command.to_source('You drop %s.' % o.name)
        command.to_room('%s drops %s.' % (command.source.name, o.name))


@syntax ("throw I.PORTABLE [at] CHARACTER")
@syntax ("throw I.PORTABLE [to] DIRECTION")
@syntax ("throw I.PORTABLE [in] ENTERABLE")
@syntax ("throw I.PORTABLE out")
@syntax ("throw I.PORTABLE out [of] ENTERABLE")
# TODO. support for passing objects through windows,
# TODO. or other impassible objects
def throw(command):
    """
    """
    pass


@syntax ("put PORTABLE in CONTAINER")
@alias  ("place")
def put(command):
    """
    """
    pass


@syntax ("empty CONTAINER")
def empty(command):
    """
    """
    pass


@syntax ("wear I.EQUIPABLE")
def wear(command):
    """
    """
    pass


@syntax ("remove E.EQUIPABLE")
@syntax ("remove PORTABLE from CONTAINER")
def remove(command):
    """
    """
    pass


@syntax ("wield I.WEAPON")
def wield(command):
    """
    """
    pass


@syntax ("unwield E.WEAPON", "remove")
def unwield(command):
    """
    """
    pass


@syntax ("use USABLE")
@syntax ("use USABLE [with] OBJECT")
@syntax ("use OBJECT [with] USABLE")
def use(command):
    """
    """
    pass


@syntax ("open OPENABLE")
def open(command):
    """
    """
    pass


@syntax ("close OPENABLE")
def close(command):
    """
    """
    pass


@syntax ("give I.PORTABLE [to] CHARACTER")
@syntax ("give CHARACTER I.PORTABLE")
@alias  ("pass")
def give(command):
    """
    """
    pass
