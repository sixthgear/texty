"""
Interaction commands.
"""
from texty.engine.command import command, syntax

@syntax  ("get R.PORTABLE")
@syntax  ("get PORTABLE in|from|inside CONTAINER")
@command ("get", "pick up", "grab", "take")
def get(command, verb, object, prep, complement):
    """
    Get an object from the room.
    """
    # resolve objects
    if complement:
        if prep in ['in' 'from', 'inside']:
            # container
            c = command.resolve(complement)
            if not c:
                a = complement.get('indef') or complement.get('spec') or 'a'
                return command.response('You don\'t see {} {} here.'.format(a, complement['noun']))
            if not hasattr(c, 'contents'):
                return command.response('{} is not a container.'.format(a, complement['noun']))
            # get something from container
            o = command.resolve(object, container=c, scope='IN')
        else:
            return command.response('You can\'t %s %s <b>%s</b> something.' % (verb, object['noun'], prep))

    elif prep:
        return command.response('That doesn\'t make sense.')

    elif object:
        o = command.resolve(object, scope='O')

    else:
        return command.response('What do you want to get?')

    if not o:
        # resolution failed
        n = object['noun']
        a = object.get('indef') or object.get('spec') or 'a'
        adj = str.join(', ', object.get('adjl', []))
        return command.response('You don\'t see {} {} {} here.'.format(a, adj, n))

    command.source.inventory.append(o)
    command.source.sidebar()
    command.room.objects.remove(o)
    command.to_source('A:You take %s.' % o.name)
    command.to_room('A:%s takes %s.' % (command.source.name, o.name))

@syntax  ("drop I.PORTABLE")
@syntax  ("drop I.PORTABLE [on] FLOOR", "put | throw")
@command ("drop", "leave")
def drop(command, verb, object, prep, complement):
    """
    Put an object from the room.
    """
    # resolve objects
    if complement:
        return command.response('That doesn\'t make sense.')

    elif prep:
        return command.response('That doesn\'t make sense.')

    elif object:
        o = command.resolve(object, scope='I')

    else:
        return command.response('What do you want to get?')

    if not o:
        # resolution failed
        n = object['noun']
        a = object.get('indef') or object.get('spec') or 'a'
        return command.response('You don\'t have {} {}.'.format(a, n))

    command.source.inventory.remove(o)
    command.source.sidebar()
    command.room.objects.append(o)
    command.to_source('A:You drop %s.' % o.name)
    command.to_room('A:%s drop %s.' % (command.source.name, o.name))







# @syntax ("throw I.PORTABLE [at] CHARACTER")
# @syntax ("throw I.PORTABLE [to] DIRECTION")
# @syntax ("throw I.PORTABLE [in] ENTERABLE")
# @syntax ("throw I.PORTABLE out")
# @syntax ("throw I.PORTABLE out [of] ENTERABLE")
# # TODO. support for passing objects through windows,
# # TODO. or other impassible objects
# def throw(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("put PORTABLE in CONTAINER")
# @alias  ("place")
# def put(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("empty CONTAINER")
# def empty(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("wear I.EQUIPABLE")
# def wear(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("remove E.EQUIPABLE")
# @syntax ("remove PORTABLE from CONTAINER")
# def remove(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("wield I.WEAPON")
# def wield(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("unwield E.WEAPON", "remove")
# def unwield(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("use USABLE")
# @syntax ("use USABLE [with] OBJECT")
# @syntax ("use OBJECT [with] USABLE")
# def use(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("open OPENABLE")
# def open(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("close OPENABLE")
# def close(command, verb, object, prep, complement):
#     """
#     """
#     pass


# @syntax ("give I.PORTABLE [to] CHARACTER")
# @syntax ("give CHARACTER I.PORTABLE")
# @alias  ("pass")
# def give(command, verb, object, prep, complement):
#     """
#     """
#     pass
