"""
Combat commands.
"""
from texty.engine.command import SCOPE, command, syntax
from texty.util.exceptions import TextyException
from texty.util.enums import EQ_PARTS, CHAR_STATE
from texty.util import serialize
from texty.util.english import STR

# @syntax ("load")
# @syntax ("load I.AMMO")
# @syntax ("load MY.WEAPON")
# @syntax ("load I.AMMO [in] MY.WEAPON", "use, put")
# @syntax ("load MY.WEAPON [with] I.AMMO", "use")
@command ("load", "reload", "r")
def load(cmd, verb, object, prep, complement):
    """
    Load a weapon with ammunition.
    raise TextyException('Quit breaking things kaptin.')
    "You don't have one of those."
    "What do you want to load?"
    "What do you want to load it in?"

    "You need to load {} into a <b>{x}</b>."
    "{y} doesn't seem to fit in {x}."
    """

    # command form D. VERB OBJECT PREP COMPLEMENT.
    if (verb and object and complement and prep in ('on', 'in', 'into', 'inside', 'with', 'using')):
        valid, msg, x, y = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.HAS),                      "You don't have {x}."),
            (lambda x,_: x.is_any('ammo loadable'),                 "You can't load {x}."),
            (lambda _,y: y.resolve(SCOPE.HAS),                      "You don't have {y}."),
            (lambda _,y: y.is_any('ammo loadable'),                 "You can't load {y}."),
            (lambda x,y: (y.is_a('ammo') and not x.is_a('ammo')) or \
                (y.is_a('loadable') and not x.is_a('loadable')),    "You can't load {x} and {y} together."),
            (lambda x,y: x.allows('load'),                          "You can't load {x} with {y}. {R}"),
            (lambda x,y: y.allows('load'),                          "You can't load {y} with {x}. {R}"),
            (lambda x,y: True,                                      "")
        )
        if x.is_a('loadable'):
            weapon, ammo = x.obj, y.obj
        else:
            weapon, ammo = y.obj, x.obj

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    elif (verb and object):
        valid, msg, x, y = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.HAS),                      "You don't have {x}."),
            (lambda x,_: x.is_any('loadable ammo'),                 "You can't load {x}."),
            (lambda x,_: x.allows('load'),                          "You can't load {x}. {R}"),
            (lambda x,_: True,                                      "")
        )
        if x.is_a('loadable'):
            weapon, ammo = x.obj, None
        else:
            weapon, ammo = None, x.obj

    # command form A. VERB.
    elif verb:
        weapon, ammo = None, None

    else:
        raise TextyException("That doesn't make ANY sense.")


    if not weapon and not ammo:
        # no weapon or ammo, so grab one from the eq
        weapon = cmd.source.equipment.first(None, attribute='loadable')
        if not weapon:
            raise TextyException("What would you like to load?")

    if weapon and not ammo:
        # look for the first ammo in inventory that fits weapon
        condition = lambda y: weapon.__class__ in y.fits
        ammo = cmd.source.inventory.first(None, attribute='ammo', condition=condition)
        if not ammo:
            raise TextyException("You don't have any ammunition for {}.".format(weapon.name))

    elif ammo and not weapon:
        # look for the first weapon in equipment that fits ammo
        condition = lambda y: y.__class__ in ammo.fits
        weapon = cmd.source.equipment.first(None, attribute='loadable', condition=condition)
        if not weapon:
            raise TextyException("You aren't using a weapon that takes {}.".format(str(x)))

    weapon.load(ammo)
    cmd.source.inventory.remove(ammo)
    cmd.source.send(serialize.full_character(cmd.source))
    cmd.to_node('A:{} loads <b>{y}</b> into <b>{x}</b>. <span class=\"sound-3x\">CHHK-CHHK!!</span>'.format(cmd.source.name, x=str(weapon.name), y=str(ammo.name)))
    return cmd.response("You load <b>{y}</b> into <b>{x}</b>. <span class=\"sound-3x\">CHHK-CHHK!!</span>".format(x=str(weapon.name), y=str(ammo.name)))



# @syntax ("unload MY.WEAPON")
@command ("unload", "unl")
def unload(cmd, verb, object, prep, complement):
    """
    Remove ammunition from a weapon.
    """
        # command form D. VERB OBJECT PREP COMPLEMENT.
    if verb and object and complement and prep in ('from'):
        valid, msg, x, y = cmd.rules(
            (lambda _,y: y.resolve(SCOPE.HAS),                      "You don't have {y}."),
            (lambda _,y: y.is_a('loadable'),                        "You can't unload {y}."),
            (lambda x,y: x.resolve(SCOPE.IN, y),                    "{y} isn't loaded with {x}."),
            (lambda x,y: x.allows('unload'),                        "You can't unload {y} from {x}. {R}"),
            (lambda x,y: y.allows('unload'),                        "You can't unload {y} from {x}. {R}"),
            (lambda x,y: True,                                      "")
        )
        weapon, ammo = y.obj, x.obj

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep:
        raise TextyException("That doesn't make sense.")

    # command form B. VERB OBJECT.
    elif verb and object:
        valid, msg, x, y = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.HAS),                      "You don't have {x}."),
            (lambda x,_: x.is_a('loadable'),                        "You can't unload {x}."),
            (lambda x,_: x.allows('unload'),                        "You can't unload {x}. {R}"),
            (lambda x,_: True,                                      "")
        )
        weapon, ammo = x.obj, None

    # command form A. VERB.
    elif verb:
        weapon, ammo = None, None
        weapon = cmd.source.equipment.first(None, attribute='loadable')
        if not weapon:
            raise TextyException("You aren't holding an unloadable weapon.")

    else:
        raise TextyException("That doesn't make ANY sense.")

    ammo = weapon.unload()
    cmd.source.inventory.append(ammo)
    cmd.source.send(serialize.full_character(cmd.source))
    cmd.to_node('A:{} unloads <b>{x}</b> from <b>{y}</b>.'.format(cmd.source.name, x=str(ammo.name), y=str(weapon.name)))
    return cmd.response("You unload <b>{x}</b> from <b>{y}</b>.".format(x=str(ammo.name), y=str(weapon.name)))


@command  ("ready", "fight", "raise")
def ready(cmd, verb, object, prep, complement):

    weapons = [x.shortname for x in cmd.source.equipment if x.is_a('wieldable')]

    if not weapons:
        raise TextyException("You aren't holding a weapon to ready.")

    weapon = str.join('</b> and <b>', weapons)

    cmd.source.state = CHAR_STATE.READY
    cmd.to_node('A:' + STR.T(STR.FIGHT.ready, cmd.source, extra={'weapon': weapon}))
    return cmd.response(STR.T(STR.FIGHT.ready, cmd.source, source=cmd.source, extra={'weapon': weapon}))

# @syntax ("kill")
# @syntax ("kill CHARACTER")
# @syntax ("kill CHARACTER [with] MY.WEAPON")
@command  ("kill", "attack", "shoot", "fire at")
def kill(cmd, verb, object, prep, complement):
    """
    """

    if complement:
        pass

    elif prep:
        pass

    elif object:
        pass

    elif verb:
        raise TextyException('Whom would you like to kill?')

    else:
        pass

    if cmd.source.status != CHAR_STATE.READY:
        ready(cmd, verb, object, prep, complement)




# @syntax ("hit R.OBJECT")
@command  ("hit", "bash", "swing", "jab", "slash")
def hit(cmd, verb, object, prep, complement):
    """
    Use a melee weapon
    """
    raise TextyException('Unfortunately, you appear to be a pacifist.')
    pass


# @syntax ("hit R.OBJECT")
@command  ("stop", "cease fire", "hold fire")
def stop(cmd, verb, object, prep, complement):
    """
    Use a melee weapon
    """
    raise TextyException('OK!')
    pass


# @syntax ("flee")
# @syntax ("flee [to] EXIT")
@command  ("flee", "run")
def flee(command, verb, object, prep, complement):
    """
    """
    pass


# @syntax ("pull [PIN] [from] I.EXPLOSIVE")
@command ("pull")
def pull(command, verb, object, prep, complement):
    """
    Pulls a pin from an explosive.
    """
    pass

