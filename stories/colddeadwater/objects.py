from texty.builtins.objects import *

class Model70(Rifle):
    name = "a Winchester Model 70 bolt action rifle"
    shortname = "Winchester Rifler"
    description = "This old rifle looks a little beat up, but you bet that it probably still works."
    nouns = 'winchester m70'
    adjectives = 'old'
    capacity = 5 # rounds
    rate = 1 # per second
    range = 10 # feet

class MP5(SubMachineGun):
    name = "a MP5 submachine gun"
    shortname = "MP5 SMG"
    description = "Small, black and lethal."
    nouns = 'mp5 mp5k'
    adjectives = 'small black lethal'
    capacity = 30
    rate = 13
    range = 50

class Crowbar(MeleeWeapon):
    name = "a large red crowbar"
    shortname = "Crowbar"
    description = "This crowbar is red, blunt and heavy. Gordon would be proud."
    nouns = "crowbar"
    adjectives = 'large red heavy blunt'
    rate = 1

class Frag(Grenade):
    name = "a fragmentation grenade"
    shortname = "Frag Grenade"
    description = "These grenades pack a punch. You make a mental note to stay well clear after the pin is pulled."
    nouns = ''
    adjectives = 'frag fragmentation'

class BoxRifleCartridges(Box, Ammo):
    name = "a small box of rifle cartridges"
    shortname = "Rifle Ammo Box"
    description = "A small box containing 20 Winchester Short Magnum cartridges. These should work nicely in a Winchester Model 70."
    nouns = 'cartridges'
    adjectives = 'winchester short magnum'
    fits = (Model70,)

class Magazine9mm(Ammo):
    name = "a 9mm magazine"
    shortname = "9mm Magazine"
    description = "A 30-round magazine. This should fit nicely in a MP5."
    nouns = 'magazine mag'
    adjectives = '9mm'
    fits = (MP5,)

class Radio(Portable):
    name = "a small shortwave radio"
    shortname = "Radio"
    description = "A small, battery operated, shortwave radio. This might be useful for communicating with other survivors."
    nouns = 'radio'
    adjectives = 'small shortwave'
    icon = 'fa-calendar-o'
    def use(self, command):
        pass

class PowerMoves(Portable):
    name = 'a copy of "Power Moves"'
    shortname = 'Power Moves'
    description = 'dforsyth\'s autobiography'
    nouns = 'power moves book'
    adjectives = ''
    icon = 'fa-book'
    def use(self, command):
        pass
