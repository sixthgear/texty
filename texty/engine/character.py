from collections import OrderedDict
from texty.builtins.characters import body
from texty.builtins.states.player import RelaxedState
from texty.engine.command import Command
from texty.engine.obj import BaseObject
from texty.util import objectlist, english
from texty.util.enums import EQ_PARTS, CHAR_STATE, CHAR_FLAG
from texty.util.exceptions import TextyException
from texty.util.english import STR
from texty.util import serialize

class Character(BaseObject):
    """
    Base character class, from which all other character classes are inherited from
    """
    # info
    name            = 'Mr. Character'
    gender          = 'N'
    occupation      = ''
    activity        = ''
    description     = '{He} looks about as ready to kill you as anyone else here.'
    attributes      = 'character'
    # stats
    hp              = 100
    capacity        = 20
    strength        = 0
    dexterity       = 0
    intelligence    = 0
    # simple lists provide templates to instantiate
    inventory       = []
    equipment       = {}

    def __init__(self, name=None, node=None):

        # copy data from class on init. This lets us reset the character to
        # initial values if required by calling __init__ again.
        self.name = name or self.__class__.name
        self.description = english.STR.T(self.__class__.description, subject=self)
        self.hp = self.__class__.hp

        self.node = node

        # the state stacks!
        self.state = [RelaxedState(self)]

        # instantiate classes from inventory list upon init.
        self.inventory = objectlist((x() for x in self.__class__.inventory))

        # equipment is the searchable object list containing everything the character is
        # currently wielding/wearing.
        self.equipment = objectlist()

        # eq_map is the mapping from EQ_PARTS enum to the object.
        self.eq_map = OrderedDict(((x, None) for x in EQ_PARTS))

        for eq, x in self.__class__.equipment.items():
            obj = x()
            self.equipment.append(obj)
            self.eq_map[eq] = obj

        self.attributes = self.__class__.attributes.copy()
        self.activity = self.__class__.activity



    @property
    def icon(self):
        if self.gender in ('M', 'N'):
            return 'icon-man'
        elif self.gender == 'F':
            return 'icon-woman'
        else:
            return ''

    @property
    def display(self):
        if self.is_a('dead'):
            return 'the corpse of {x.name}'.format(x=self)
        elif self.occupation:
            return '{x.first} the {x.occupation}'.format(x=self)
        else:
            return '{x.name}'.format(x=self)

    @property
    def first(self):
        return self.name.split()[0].capitalize()

    @property
    def inv_weight(self):
        weight = 0
        for i in self.inventory:
            weight += i.weight
        return weight

    def do(self, command, echo=False):
        """
        Parse and execute a text command for this player.
        """
        Command(source=self, command=command, echo=echo).run()

    def send(self, message):
        """
        By default, do nothing. Not all characters are players (ie. they don't need to see output)
        """
        pass

    def get(self, object, container):
        self.trigger('get', object=object, container=container)

    def drop(self, object, node):
        self.trigger('drop', object=object, node=node)

    def put(self, object, container):
        self.trigger('put', object=object, container=container)

    def give(self, object, character):
        self.trigger('give', object=object, character=character)

    def use(self, object):
        self.trigger('use', object=object)

    def eat(self, object):
        self.trigger('eat', object=object)

    def load(self, weapon=None, ammo=None):

        if not weapon and not ammo:
            # no weapon or ammo, so grab one from the eq
            weapon = self.equipment.first(None, attribute='loadable')
            if not weapon:
                raise TextyException("What would you like to load?")

        if weapon and not ammo:
            # look for the first ammo in inventory that fits weapon
            condition = lambda y: weapon.__class__ in y.fits
            ammo = self.inventory.first(None, attribute='ammo', condition=condition)
            if not ammo:
                raise TextyException("You don't have any ammunition for {}.".format(weapon.name))

        elif ammo and not weapon:
            # look for the first weapon in equipment that fits ammo
            condition = lambda y: y.__class__ in ammo.fits
            weapon = self.equipment.first(None, attribute='loadable', condition=condition)
            if not weapon:
                raise TextyException("You aren't using a weapon that takes {}.".format(str(x)))

        weapon.load(ammo)
        self.inventory.remove(ammo)
        self.send(serialize.full_character(self))

        extra = {
            'weapon': weapon.name,
            'ammo': ammo.name
        }
        self.node.send(STR.T(STR.FIGHT.load, self, extra=extra), source=self)
        self.send(STR.T(STR.FIGHT.load, self, source=self, extra=extra))

        self.trigger('load', weapon=weapon, ammo=ammo)

    def unload(self, weapon=None, ammo=None):

        if not weapon:
            weapon = self.equipment.first(None, attribute='loadable')
            if not weapon:
                raise TextyException("You aren't holding an unloadable weapon.")

        ammo = weapon.unload()

        self.inventory.append(ammo)
        self.send(serialize.full_character(self))
        extra = {
            'weapon': weapon.name,
            'ammo': ammo.name
        }
        self.node.send(STR.T(STR.FIGHT.unload, self, extra=extra), source=self)
        self.send(STR.T(STR.FIGHT.unload, self, source=self, extra=extra))
        self.trigger('unload', weapon=weapon)

    def ready(self):
        """
        Make oneself ready to fight.
        """
        if not self.weapon:
            raise TextyException("You aren't holding a weapon to ready.")

        extra = {
            'weapon': self.weapon.name
        }

        self.node.send(STR.T(STR.FIGHT.ready, self, extra=extra), source=self)
        self.send(STR.T(STR.FIGHT.ready, self, source=self, extra=extra))

        self.trigger('ready')


    def hurt(self, damage):
        self.send('<span class="sound-3x">OUCH!</span>')
        self.hp -= damage
        self.trigger('hurt', damage)

    def target(self, target):
        """
        Set a monster or character to be the target.
        """
        if not self.weapon:
            raise TextyException('You aren\'t holding a weapon!')

        if target.is_a('player'):
            raise TextyException('Don\'t kill other players just yet, it doesn\'t work well.')

        if not self.weapon.ammo:
            raise TextyException('Your {weapon.shortname} isn\'t loaded!'.format(weapon=self.weapon))

        self.trigger('target', target=target)
        target.trigger('targetted', target=self)
        return True

    def untarget(self):
        self.trigger('untarget')

    def attack(self, target):
        """
        Perform an attack. This method is scheduled by the state machine.
        """
        if self.weapon.is_a('gun'):
            self.weapon.fire(self, target)

        elif self.weapon.is_a('melee'):
            self.weapon.swing()

        self.trigger('attack', target=target)
        target.trigger('attacked', target=self)

    def fall(self):
        self.node.send('A:' + STR.T(STR.FIGHT.fall, self))
        self.trigger('fall')

    def die(self):
        self.node.send('A:' + STR.T(STR.FIGHT.death, self))
        self.trigger('death')
        self.attributes.remove('character')
        self.attributes.add('dead')
        self.node.characters.remove(self)
        self.node.objects.append(self)
        self.events = {}


    def on_fire(self, weapon, ammo, rounds, source, target):
        """
        Weapon has fired.
        """
        extra = {
            'amount': rounds,
            'weapon': self.weapon,
            'target': target.display
        }

        msg_A = STR.T(STR.FIGHT.fire_A, self, source=self, extra=extra)
        msg_B = '<span class="sound-2x">{sound}</span'.format(sound=weapon.sound(rounds))

        self.send('A:' + msg_A + msg_B)

    def on_empty(self, weapon):
        self.send('A: <span class=\"sound-3x\">&mdash;CLICK&mdash;</span>')
        self.trigger('weapon_empty', weapon)

    def stop(self):
        """
        Stop whatever you were doing.
        """
        self.trigger('stop')

    def flee(self):
        self.trigger('flee')

    @property
    def weapon(self):

        holding = self.eq_map.get(EQ_PARTS.L_HAND) or self.eq_map.get(EQ_PARTS.R_HAND)

        if holding and holding.is_a('wieldable'):
            return holding
        else:
            return None



    def equip(self, object, parts=None):
        """
        Take reference to object and assign it to characters equipment slots.
        """
        # first check if this object is equipable
        if not object.is_a('equipable'):
            raise TextyException('{} is not equipable.'.format(object.name))

        # next make sure if it has defined a "fits" list.
        if not object.fits:
            raise TextyException('{} does not fit anything.'.format(object.name))

        # use the "fits" list if no specific parts specified
        if not parts:
            parts = object.fits

        # try each part
        for part in parts:

            if part not in object.fits:
                raise TextyException('It doesn\'t fit there.')

            if not self.eq_map.get(part):
                self.eq_map[part] = object
                self.equipment.append(object)
                self.trigger('equip', object=object, part=part)
                if object.is_a('gun'):
                    object.register('fire', self.on_fire)
                    object.register('empty', self.on_empty)
                return True


        # tried to equip object in all supplied positions, didn't work.
        raise TextyException('You already have something there.'.format(object.name))

    def unequip(self, object, parts=None):
        """
        Take thing off
        """
        if not parts:
            parts = object.fits

        for part, eq in self.eq_map.items():
            if eq == object:
                self.eq_map[part] = None
                self.equipment.remove(object)
                self.trigger('unequip', object=object, part=part)
                if object.is_a('gun'):
                    object.unregister('fire', self.on_fire)
                    object.unregister('empty', self.on_empty)
                return True

        raise TextyException('Couldn\'t Unequip {}.'.format(object.name))

    def move_toward(self, target, direction):
        self.trigger('move', target, direction)

    def move_to(self, node):
        """
        Move this character to a different node. This can be called by command functions or as
        an internal call. The calling function is reponsible to send notifications.
        Use None to remove the player from all rooms.
        """
        # first remove this player from the rooms characters list
        if self.node and self in self.node.characters:
            self.node.exit(self)
            # self.node.characters.remove(self)
        # next change the players node reference, and then add to the new node's character list
        if node:
            self.node = node
            if self.is_a('player'):
                # self.node.characters.insert(0, self)
                self.node.enter(self)
            else:
                self.node.enter(self)
                # self.node.characters.append(self)
