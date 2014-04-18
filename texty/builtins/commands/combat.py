"""
Combat commands.
"""
from texty.engine.command import syntax, alias
from texty.builtins.objects import RangedWeapon, Ammo

@syntax ("load")
@syntax ("load I.AMMO")
@syntax ("load MY.WEAPON")
@syntax ("load I.AMMO [in] MY.WEAPON", "use, put")
@syntax ("load MY.WEAPON [with] I.AMMO", "use")
def load(command):
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



@syntax ("unload")
@syntax ("unload MY.WEAPON")
def unload(command):
    """
    Remove ammunition from a weapon.
    """
    pass


@syntax ("pull [PIN] [from] I.EXPLOSIVE")
def pull(command):
    """
    Pulls a pin from an explosive.
    """
    pass


@syntax ("kill")
@syntax ("kill CHARACTER")
@syntax ("kill CHARACTER [with] MY.WEAPON")
@alias  ("attack")
def kill(command):
    """
    """
    pass


@syntax ("shoot [at] R.OBJECT")
@alias  ("fire")
def kill(command):
    """
    Shoot a ranged weapon.
    """
    pass


@syntax ("hit R.OBJECT")
@alias  ("bash", "swing", "jab", "slash")
def hit(command):
    """
    Use a melee weapon
    """
    pass


@syntax ("flee")
@syntax ("flee [to] EXIT")
@alias  ("run [away]")
def flee(command):
    """
    """
    pass


