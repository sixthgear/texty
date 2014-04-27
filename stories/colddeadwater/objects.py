from texty.builtins.objects import *
from texty.util.enums import EQ_PARTS

class Model70(Rifle):
    """
    a Winchester Model 70 bolt action rifle
    ---
    This old rifle looks a little beat up, but you bet that it probably still works.
    """
    shortname = "Winchester Rifle"
    adjectives = 'old winchester bolt action'
    nouns = 'rifle m70'
    # -- ammo
    capacity = 5 # rounds
    rate = 1 # per second
    range = 10 # feet
    fits = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)

class MP5(SubMachineGun):
    """
    a Heckler & Koch MP5 submachine gun
    ---
    Small, black and lethal.
    """
    shortname = "H&K MP5 submachine gun"
    adjectives = 'small black lethal heckler koch'
    nouns = 'mp5 mp5k'
    # -- ammo
    rate = 13
    range = 50
    fits = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)

class Crowbar(MeleeWeapon):
    """
    a large red crowbar
    ---
    This crowbar is red, blunt and heavy. Gordon would be proud.
    """
    shortname = "Crowbar"
    adjectives = 'large red heavy blunt'
    nouns = "crowbar"
    # -- melee
    rate = 1
    fits = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)

class Frag(Grenade):
    """
    a fragmentation grenade
    ---
    These grenades pack a punch. You make a mental note to stay well clear after the pin is pulled.
    """
    shortname = "Frag Grenade"
    adjectives = 'frag fragmentation'
    nouns = 'grenade'

class BoxRifleCartridges(Ammo):
    """
    a small box of rifle shells
    ---
    A small box containing 20 Winchester Short Magnum shells. These should work nicely in
    a Winchester Model 70.
    """
    shortname = "Box Rifle Shells"
    adjectives = 'winchester short magnum'
    nouns = 'cartridges shells box'
    # --- ammo
    fits = (Model70,)
    item = 'shell'
    capacity = 20

class Magazine9mm(Ammo):
    """
    a 9mm magazine
    ---
    A 30-round magazine. This should fit nicely in a MP5.
    """
    shortname = '9mm Magazine'
    adjectives = '9mm'
    nouns = 'magazine mag'
    # --- amo
    fits = (MP5,)
    item = 'bullet'
    capacity = 30

class Radio(Portable):
    """
    a small shortwave radio
    ---
    A small, battery operated, shortwave radio. This might be useful for communicating
    with other survivors.
    """
    shortname = 'Radio'
    adjectives = 'small shortwave'
    nouns = 'radio'
    icon = 'icon-radio'

    def use(self, command):
        pass

class PowerMoves(Portable):
    """
    a copy of "Power Moves"
    ---
    D. Forsyth's autobiography. The book contains a number of powerful moves you can perform in
    various social and/or combat situations.
    """
    shortname = 'Power Moves'
    adjectives = 'power'
    nouns = 'moves book'
    icon = 'icon-book2'

    def use(self, command):
        pass


class Tshirt(Equipable):
    """
    a leftover t-shirt from your failed startup
    ---
    It features your startup's vowel-less name in bold Helvetica Neue beside a suitably minamilist
    logo of vague geometric figures.
    """
    shortname = 'Startup T-shirt'
    adjectives = 'startup'
    nouns = 'shirt t-shirt tshirt'
    icon = 'icon-tshirt'
    # ---
    fits = (EQ_PARTS.BODY,)

class FreeBSDshirt(Tshirt):
    """
    a FreeBSD t-shirt
    ---
    It has the FreeBSD Daemon on the front!
    """
    shortname = 'FreeBSD T-shirt'
    adjectives = 'freebsd'
    nouns = ''
    icon = 'icon-tshirt'
    # ---


class RippedJeans(Equipable):
    """
    a pair of unintentionally ripped jeans
    ---
    You're sure these jeans were not ripped when they were bought, but have no idea when it
    actually happened.
    """
    shortname = 'Ripped Jeans'
    adjectives = 'ripped'
    nouns = 'jeans pants'
    icon = 'icon-hanger'
    # ---
    fits = (EQ_PARTS.LEGS,)

class LeatherBoots(Equipable):
    """
    a fine pair of leather boots
    ---
    These look like some great boots.
    """
    shortname = 'Leather Boots'
    adjectives = 'leather'
    nouns = 'boot'
    icon = 'icon-hanger'
    # ---
    fits = (EQ_PARTS.FEET,)

class MotorcycleHelmet(Equipable):
    """
    a tinted, black motorcycle helmet
    ---
    You might not die if you fell off a motorcycle while wearing this.
    """
    shortname = 'Motorcycle Helmet'
    adjectives = 'motorcycle'
    nouns = 'helmet'
    icon = 'icon-hanger'
    # ---
    fits = (EQ_PARTS.HEAD,)

class CivilWarTrenchcoat(Equipable):
    """
    a blue civil war era trenchcoat
    ---
    Its blue and old.
    """
    shortname = 'Civil War Trenchcoat'
    adjectives = 'civil war trench blue'
    nouns = 'trenchcoat coat'
    icon = 'icon-tshirt'
    # ---
    fits = (EQ_PARTS.SHOULDERS,)

class VibramFivefinger(Equipable):
    """
    a single Vibram Fivefingers shoe
    ---
    It's green and looks ridiculous. It's for the left foot.
    """
    shortname = 'Single Vibram Shoe'
    adjectives = 'green vibram fivefingers'
    nouns = 'shoe'
    icon = 'icon-hanger'
    # ---
    fits = (EQ_PARTS.FEET,)

class ClifBar(Food):
    """
    an orginal Clif Bar&trade;
    ---
    The slick packaging makes you believe this is probably healthy for you. You consider a diet of
    only Clif Bars&trade;.
    """
    shortname = 'Clif Bar&trade;'
    adjectives = 'clif'
    nouns = 'bar'
    icon = 'icon-ticket'


class Burrito(Food):
    """
    a mission-style burrito
    ---
    It looks fucking delicious.
    """
    shortname = 'Burrito'
    adjectives = 'mission mission-style'
    nouns = 'burrito'
    icon = 'icon-food'


class Crate(Box):
    """
    a shockingly generic crate
    ---
    This is your standard videogame crate. Shockingly so. The texture looks really flat and it\'s
    just sitting there looking really generic and stuff.
    """
    shortname = 'Crate'
    adjectives = 'shockingly generic'
    nouns = 'crate'
    icon = 'icon-box2'
    contents = [PowerMoves] * 10 + [ClifBar] * 2
