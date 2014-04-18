from texty.builtins.objects import *

class Model70(Rifle):
    name = "a Winchester Model 70 bolt action rifle"
    shortname = "Wincheste Rifler"
    description = "This old rifle looks a little beat up, but you bet that it probably still works."
    keywords = 'winchester model m70'
    capacity = 5 # rounds
    rate = 1 # per second
    range = 10 # feet

class MP5(SubMachineGun):
    name = "a MP5 submachine gun"
    shortname = "MP5 SMG"
    description = "Small, black and lethal."
    keywords = 'mp5k'
    capacity = 30
    rate = 13
    range = 50

class Crowbar(MeleeWeapon):
    name = "a large red crowbar"
    shortname = "Crowbar"
    description = "This crowbar is red, blunt and heavy. Gordon would be proud."
    keywords = "crowbar"
    rate = 1

class Frag(Grenade):
    name = "a fragmentation grenade"
    shortname = "Frag Grenade"
    description = "These grenades pack a punch. You make a mental note to stay well clear after the pin is pulled."
    keywords = 'frag'

class BoxRifleCartridges(Box, Ammo):
    name = "a small box of rifle cartridges"
    shortname = "Rifle Ammo Box"
    description = "A small box containing 20 Winchester Short Magnum cartridges. These should work nicely in a Winchester Model 70."
    keywords = 'wsm cartridges'
    fits = (Model70,)

class Magazine9mm(Ammo):
    name = "a 9mm magazine"
    shortname = "9mm Magazine"
    description = "A 30-round magazine. This should fit nicely in a MP5."
    keywords = '9mm magazine'
    fits = (MP5,)

class Radio(Portable):
    name = "a small shortwave radio"
    shortname = "Radio"
    description = "A small, battery operated, shortwave radio. This might be useful for communicating with other survivors."
    keywords = 'shortwave radio'
    icon = 'fa-calendar-o'
    def use(self, command):
        pass

class PowerMoves(Portable):
    name = 'a copy of "Power Moves"'
    shortname = 'Power Moves'
    description = 'dforsyth\'s autobiography'
    keywords = 'power moves book dforsyth autobiography'
    icon = 'fa-book'
    def use(self, command):
        pass
