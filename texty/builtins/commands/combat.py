"""
Combat commands.
"""
from texty.engine.command import command, syntax
from texty.builtins.objects import RangedWeapon, Ammo

# @syntax ("load")
# @syntax ("load I.AMMO")
# @syntax ("load MY.WEAPON")
# @syntax ("load I.AMMO [in] MY.WEAPON", "use, put")
# @syntax ("load MY.WEAPON [with] I.AMMO", "use")
@command ("load")
def load(command, verb, object, prep, complement):
    """
    Load a weapon with ammunition.
    """

    weapon, ammo = command.arguments[:2]

    if weapon == False or ammo == False:
        return command.to_source('You don\'t have one of those.')
    if (weapon, ammo) == (None, None):
        return command.to_source('What do you want to load?')
    if weapon == None:
        return command.to_source('What do you want to load it in?')
    if ammo == None:
        return command.to_source('You don\'t have any ammunition for %s.' % weapon.name)
    # if not weapon and not ammo:
    #     return command.to_source('You need to load <em>ammunition</em> into a <em>weapon</em>.')
    # if not weapon.__class__ in ammo.__class__.fits:
    #     command.to_source('%s doesn\'t seem to fit in %s.' % (ammo.name, weapon.name))
    #     return
    command.source.inventory.remove(ammo)
    weapon.ammo = ammo
    command.to_source('You load %s into %s. <em>CHHK-CHHK.</em>' % (ammo.name, weapon.name))
    command.to_room('%s loads a %s. <em>CHHK-CHHK.</em>' % (command.source.name, weapon.name))




# @syntax ("unload MY.WEAPON")
@command ("unload")
def unload(command, verb, object, prep, complement):
    """
    Remove ammunition from a weapon.
    """
    pass


# @syntax ("pull [PIN] [from] I.EXPLOSIVE")
@command ("pull")
def pull(command, verb, object, prep, complement):
    """
    Pulls a pin from an explosive.
    """
    pass


# @syntax ("kill")
# @syntax ("kill CHARACTER")
# @syntax ("kill CHARACTER [with] MY.WEAPON")
@command  ("kill", "attack")
def kill(command, verb, object, prep, complement):
    """
    """
    pass


# @syntax ("shoot [at] R.OBJECT")
@command  ("shoot", "fire")
def kill(command, verb, object, prep, complement):
    """
    Shoot a ranged weapon.
    """
    pass


# @syntax ("hit R.OBJECT")
@command  ("hit", "bash", "swing", "jab", "slash")
def hit(command, verb, object, prep, complement):
    """
    Use a melee weapon
    """
    pass


# @syntax ("flee")
# @syntax ("flee [to] EXIT")
@command  ("flee run")
def flee(command, verb, object, prep, complement):
    """
    """
    pass


