"""
Interaction commands.
"""
from texty.builtins.commands.combat import load
from texty.engine.command import SCOPE, command, syntax
from texty.engine.node import Node
from texty.util import serialize
from texty.util.exceptions import TextyException


@command ("get", "pick up", "grab", "take")
def get(cmd, verb, object, prep, complement):
    """
    Get an object from the room or other container.
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.
    if verb and object and complement and prep in ('from', 'in', 'inside'):
        valid, msg, x, y = cmd.rules(
            (lambda _,y: y.resolve(),                    "You don't see {y} here."),
            (lambda _,y: y.is_any('container node'),     "{y} is not a container."),
            (lambda x,y: x.resolve(SCOPE.IN, y),         "You don't see {x} in {y}."),
            (lambda x,y: x.is_a('portable'),             "You can't remove {x} from {y}."),
            (lambda x,y: x.allows('get'),                "You can't remove {x} from {y}. {R}"),
            (lambda x,y: y.allows('get'),                "You can't remove {x} from {y}. {R}"),
            (lambda x,y: True,                           "You get {x} from {y}.")
        )

        # get an object from within another object
        if isinstance(y, Node):
            y.obj.objects.remove(x.obj)
        else:
            y.obj.contents.remove(x.obj)

        cmd.source.inventory.append(x.obj)

        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} takes {} from {}.'.format(cmd.source.name, str(x), str(y)))
        return cmd.response(msg)

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    elif verb and object:
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.ROOM),         "You don't see {x} here."),
            (lambda x,_: x.is_a('portable'),            "{x} is far too heavy to move."),
            (lambda x,_: x.allows('get'),               "You can't take {x}. {R}"),
            (lambda x,_: True,                          "You take {x}."),
        )
        # get an object from the room
        cmd.node.objects.remove(x.obj)
        cmd.source.inventory.append(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} takes {}.'.format(cmd.source.name, str(x)))
        return cmd.response(msg)

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to get?")

    raise TextyException("That doesn't make ANY sense.")


@command ("drop", "throw away")
def drop(cmd, verb, object, prep, complement):
    """
    Put an object in the room.
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.
    if verb and object and complement:
        raise TextyException("That doesn't make sense.")

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    elif verb and object:
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.INV),          "You don't have {x}."),
            # (lambda x,_: x.is_a('portable'),            "You can't drop {x}."),
            (lambda x,_: x.allows('drop'),              "You can't drop {x}. {R}"),
            (lambda x,_: True,                          "You drop {x}.")
        )
        # drop an object in the room
        cmd.source.inventory.remove(x.obj)

        if x.obj.is_a('character'):
            cmd.node.characters.append(x.obj)
        else:
            cmd.node.objects.append(x.obj)
            cmd.node.sort()

        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} drops {}.'.format(cmd.source.name, str(x)))
        return cmd.response(msg)

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to drop?")

    raise TextyException("That doesn't make ANY sense.")


@command ("put", "place")
def put(cmd, verb, object, prep, complement):
    """
    put PORTABLE in CONTAINER
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.
    # command form B. VERB OBJECT.
    if (verb and object and complement and prep in ('in', 'into', 'inside')) or (verb and object and not prep):
        valid, msg, x, y = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.INV),           "You don't have {x}."),
            # (lambda x,_: x.is_any('portable'),           "You can't move {x}."),
            (lambda x,y: y.provided(),                   "What do you want to put {x} in?"),
            (lambda _,y: y.resolve(),                    "You don't see {y}."),
            (lambda _,y: y.is_any('container loadable'), "{y} is not a container."),
            (lambda x,y: x.allows('put'),                "You can't put {x} into {y}. {R}"),
            (lambda x,y: y.allows('put'),                "You can't put {x} into {y}. {R}"),
            (lambda x,y: True,                           "You put {x} into {y}.")
        )

        if x.is_a('ammo') and y.is_a('loadable'):
            from . combat import load
            return load(cmd, 'load', object, 'in', complement)
            # cmd.enqueue('load {} in {}'.format())

        cmd.source.inventory.remove(x.obj)
        y.obj.contents.append(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} puts {} into {}.'.format(cmd.source.name, str(x), str(y)))
        return cmd.response(msg)

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to put?")

    raise TextyException("That doesn't make ANY sense.")


@command ("give")
def give(cmd, verb, object, prep, complement):
    """
    give PORTABLE to CHARACTER
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.
    # command form B. VERB OBJECT.
    if (verb and object and complement and prep in ('to')) or (verb and object and not prep):
        valid, msg, x, y = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.INV),           "You don't have {x}."),
            # (lambda x,_: x.is_a('portable'),             "You can't move {x}."),
            (lambda x,y: y.provided(),                   "Who do you want to give {x} to?"),
            (lambda _,y: y.resolve(SCOPE.ROOM),          "You don't see {y} around."),
            (lambda _,y: y.is_a('character'),            "{y} is not a person."),
            (lambda x,y: x.allows('give'),               "You can't give {x} to {y}. {R}"),
            (lambda x,y: y.allows('give'),               "You can't give {x} to {y}. {R}"),
            (lambda x,y: True,                           "You give {x} to {y}.")
        )
        cmd.source.inventory.remove(x.obj)
        y.obj.inventory.append(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))

        if y.obj.is_a('player'):
            y.obj.send(serialize.full_character(y.obj))

        cmd.to_node('A:{} gives {} to {}.'.format(cmd.source.name, str(x), str(y)))
        return cmd.response(msg)

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to give?")

    raise TextyException("That doesn't make ANY sense.")



# @syntax ("wear I.EQUIPABLE")
@command ("equip", "eq", "wear", "wield", "wi", "put on")
def equip(cmd, verb, object, prep, complement):
    """
    Equip things like a boss.
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.

    if (complement and prep in ('on', 'in')):
        valid, msg, x, y = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.INV),           "You don't have {x}."),
            (lambda x,_: x.is_a('equipable'),            "You can't equip {x}."),
            (lambda _,y: y.resolve(SCOPE.BODY),          "You don't have {y}."),
            (lambda _,y: y.is_a('bodypart'),             "{y} is not a body part."),
            (lambda x,y: x.allows('equip'),              "You can't equip {x} on your {y}. {R}"),
            (lambda x,y: y.allows('equip'),              "You can't equip {x} on your {y}. {R}"),
            (lambda x,y: True,                           "You equip {x} on your {y}.")
        )
        cmd.source.equip(x.obj, parts=[y.obj.typ])
        cmd.source.inventory.remove(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} equips {} on {}.'.format(cmd.source.name, str(x), str(y)))
        return cmd.response(msg)

    # command form C. VERB PREP OBJECT.
    elif prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    elif (object):
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.INV),           "You don't have {x}."),
            (lambda x,_: x.is_a('equipable'),            "You can't equip {x}."),
            (lambda x,_: x.allows('equip'),              "You can't equip {x}. {R}"),
            (lambda x,_: True,                           "You equip {x}.")
        )
        cmd.source.equip(x.obj)
        cmd.source.inventory.remove(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} equips {}.'.format(cmd.source.name, str(x)))
        return cmd.response(msg)

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to {}?".format(verb))

    raise TextyException("That doesn't make ANY sense.")


@command ("unequip", "take off", "unwield", "remove")
def unequip(cmd, verb, object, prep, complement):
    """
    Unequip things like a boss.
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.

    if (verb and object and complement and prep in ('from', 'in')):
        valid, msg, x, y = cmd.rules(
            (lambda _,y: y.resolve(SCOPE.BODY),          "You don't have {y}."),
            (lambda _,y: y.is_a('bodypart'),             "{y} is not a body part."),
            (lambda x,_: x.resolve(SCOPE.EQUIP),         "You aren't wearing {x}."),
            (lambda x,y: x.allows('unequip'),            "You can't remove {x} from your {y}. {R}"),
            (lambda x,y: y.allows('unequip'),            "You can't remove {x} from your {y}. {R}"),
            (lambda x,y: True,                           "You remove {x} from your {y}.")
        )
        cmd.source.unequip(x.obj, parts=[y.obj.typ])
        cmd.source.inventory.append(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} removes {} from {}.'.format(cmd.source.name, str(x), str(y)))
        return cmd.response(msg)

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    if (verb and object):
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.EQUIP),         "You aren't wearing {x}."),
            (lambda x,_: x.allows('unequip'),            "You can't remove {x}. {R}"),
            (lambda x,_: True,                           "You remove {x}.")
        )
        cmd.source.unequip(x.obj)
        cmd.source.inventory.append(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} removes {}.'.format(cmd.source.name, str(x)))
        return cmd.response(msg)

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to {}?".format(verb))

    raise TextyException("That doesn't make ANY sense.")



# @syntax ("use USABLE")
# @syntax ("use USABLE [with] OBJECT")
# @syntax ("use OBJECT [with] USABLE")
@command("use")
def use(cmd, verb, object, prep, complement):
    """
    """
    if complement:
        valid, msg, x, y = cmd.rules(
            (lambda _,y: y.resolve(SCOPE.ANY),           "You don't see {y} here."),
            (lambda x,_: x.resolve(SCOPE.ANY),           "You don't see {x} here."),
            (lambda x,y: x.allows('use'),                "You can't use {x} with {y}. {R}"),
            (lambda x,y: y.allows('use'),                "You can't use {y} with {x}. {R}"),
            (lambda x,y: True,                           "You use {x} with {y}.")
        )

        if x.is_a('usable'):
            x.obj.use(y.obj)
            return

        elif x.is_a('equipable') and x.is_a('bodypart'):
            return equip(cmd, verb, object, prep, complement)

        elif x.is_any('loadable ammo') and y.is_any('loadable ammo'):
            return load(cmd, verb, object, prep, complement)

        else:
            return cmd.response("You aren't sure how to use {x} {prep} {y}.".format(x=str(x), y=str(y), prep=prep))

    # command form C. VERB PREP OBJECT.
    elif prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    if object:
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.ANY),           "You don't see {x} here."),
            (lambda x,_: x.allows('use'),                "You can't use {x}. {R}"),
            (lambda x,_: True,                           "You use {x}.")
        )

        if x.is_a('usable'):
            x.obj.use()
            return

        elif x.is_a('equipable'):
            return equip(cmd, verb, object, None, None)

        elif x.is_any('ammo'):
            return load(cmd, verb, object, None, None)

        elif x.is_a('food'):
            return eat(cmd, verb, object, None, None)

        else:
            return cmd.response("You aren't sure how to use {x}.".format(x=str(x)))

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to {}?".format(verb))

    raise TextyException("That doesn't make ANY sense.")



@command("eat")
def eat(cmd, verb, object, prep, complement):
    """
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.
    if verb and object and complement:
        raise TextyException("That doesn't make sense.")

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    elif verb and object:
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.INV),          "You don't have {x}."),
            (lambda x,_: x.is_a('food'),                "{x} is not edible."),
            (lambda x,_: x.allows('eats'),              "You can't eat {x}. {R}"),
            (lambda x,_: True,                          "You eat {x}.")
        )
        # drop an object in the room
        x.obj.eat()
        cmd.source.inventory.remove(x.obj)
        cmd.source.send(serialize.full_character(cmd.source))
        cmd.to_node('A:{} eats {}.'.format(cmd.source.name, str(x)))
        return cmd.response(msg)

    # command form A. VERB.
    elif verb:
        raise TextyException("What would you like to eat?")

    raise TextyException("That doesn't make ANY sense.")




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

# @syntax ("empty CONTAINER")
# def empty(command, verb, object, prep, complement):
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

