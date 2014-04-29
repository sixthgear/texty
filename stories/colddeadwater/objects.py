from texty.builtins.objects import *
from texty.util.enums import EQ_PARTS
from texty.util.exceptions import TextyException

# --- MELEE WEAPONS --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Crowbar(MeleeWeapon):
    """
    a large red crowbar
    ---
    This crowbar is red, blunt and heavy. Gordon would be proud.
    """
    shortname       = 'Crowbar'
    adjectives      = 'large red heavy blunt'
    nouns           = 'crowbar'
    fits            = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)
    # -- specs
    rate            = 1

# --- EXPLOSIVE WEAPONS --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Frag(Grenade):
    """
    a fragmentation grenade
    ---
    These grenades pack a punch. You make a mental note to stay well clear after the pin is pulled.
    """
    shortname       = 'Frag Grenade'
    adjectives      = 'fragmentation'
    nouns           = 'frag grenade'

# --- RANGED WEAPONS --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Model70(Rifle):
    """
    a Winchester Model 70 bolt action rifle
    ---
    This old rifle looks a little beat up, but you bet that it probably still works.
    """
    shortname       = 'Winchester Model 70'
    adjectives      = 'bolt action model'
    nouns           = 'winchester 70 M70'
    # -- equip
    fits            = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)
    # -- specs
    capacity        = 5     # rounds
    rate            = 1     # per second
    range           = 60    # meters

class Model870(Shotgun):
    """
    a Remington Model 870 pump action shotgun
    ---
    The Remington Model 870 pump action shotgun holds the record for the best selling shotgun
    in history.
    """
    shortname       = 'Remington Model 870'
    adjectives      = 'pump action model'
    nouns           = 'remington 870 M870'
    # -- equip
    fits            = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)
    # -- specs
    capacity        = 5     # rounds
    rate            = 1     # per second
    range           = 20    # meters

class MP5(SubMachineGun):
    """
    a Heckler & Koch MP5 submachine gun
    ---
    Small, black and lethal.
    """
    shortname       = "H&K MP5 submachine gun"
    adjectives      = 'heckler koch'
    nouns           = 'mp5 mp5k'
    # -- equip
    fits            = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)
    # -- specs
    capacity        = 30    # rounds
    rate            = 13    # per second
    range           = 30    # meters

class M1911(Pistol):
    """
    A Colt M1911 semi-automatic pistol
    ---
    A Colt M1911 semi-automatic pistol looks reliable.
    """
    shortname       = 'Colt M1911 Pistol'
    adjectives      = 'colt m1911 1911 semi automatic'
    nouns           = 'colt m1911 1911'
    # -- equip
    fits            = (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND)
    # -- specs
    capacity        = 7     # rounds
    rate            = 1     # per second
    range           = 20    # meters

# --- AMMO --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class BoxRifleCartridges(Ammo):
    """
    a small box of rifle shells
    ---
    A small box containing 20 Winchester Short Magnum shells. These should work nicely in
    a Winchester Model 70.
    """
    shortname       = 'Box of Rifle Shells'
    adjectives      = 'winchester short magnum rifle'
    nouns           = 'cartridges shells box'
    # --- ammo
    fits            = (Model70,)
    capacity        = 20
    item            = 'short magnum shell'

class Box12Gauge(Ammo):
    """
    a small box of 12-gauge shotgun shells
    ---
    A small box containing 25 shotgun shells. These should work nicely in a Remington 870.
    """
    shortname       = 'Box of Shotgun Shells'
    adjectives      = 'remington 12 gauge shotgun'
    nouns           = 'cartridges shells box'
    # --- ammo
    fits            = (Model870,)
    capacity        = 25
    item            = '12-gauge shell'

class Magazine9mm(Ammo):
    """
    a 9mm magazine
    ---
    A 30-round magazine. This should fit nicely in a MP5.
    """
    shortname       = '9mm Magazine'
    adjectives      = '9mm mp5 smg '
    nouns           = 'magazine mag'
    # --- ammo
    fits            = (MP5,)
    capacity        = 30
    item            = '9mm round'

class Magazine45ACP(Ammo):
    """
    a .45 ACP Magazine
    ---
    A 7-round box magazine designed to be used with the Colt M1911.
    """
    shortname       = '.45 ACP Magazine'
    adjectives      = '45 acp colt pistol m1911 1911'
    nouns           = 'magazine mag'
    # --- ammo
    fits            = (M1911,)
    capacity        = 7
    item            = 'ACP round'

# --- CLOTHING --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Tshirt(Equipable):
    """
    a leftover t-shirt from your failed startup
    ---
    It features your startup's vowel-less name in bold Helvetica Neue beside a suitably minamilist
    logo of vague geometric figures.
    """
    shortname       = 'Startup T-shirt'
    adjectives      = 'startup'
    nouns           = 'shirt t-shirt tshirt'
    icon            = 'icon-tshirt'
    # ---
    fits            = (EQ_PARTS.BODY,)

class FreeBSDshirt(Tshirt):
    """
    a FreeBSD t-shirt
    ---
    It has the FreeBSD Daemon on the front!
    """
    shortname       = 'FreeBSD T-shirt'
    adjectives      = 'freebsd'
    nouns           = ''
    icon            = 'icon-tshirt'
    # ---
    fits            = (EQ_PARTS.BODY,)

class RippedJeans(Equipable):
    """
    a pair of unintentionally ripped jeans
    ---
    You're sure these jeans were not ripped when they were bought, but have no idea when it
    actually happened.
    """
    shortname       = 'Ripped Jeans'
    adjectives      = 'ripped'
    nouns           = 'jeans pants'
    icon            = 'icon-hanger'
    # ---
    fits            = (EQ_PARTS.LEGS,)

class LeatherBoots(Equipable):
    """
    a fine pair of leather boots
    ---
    These look like some great boots.
    """
    shortname       = 'Leather Boots'
    adjectives      = 'leather'
    nouns           = 'boot'
    icon            = 'icon-hanger'
    # ---
    fits            = (EQ_PARTS.FEET,)

class VibramFivefinger(Equipable):
    """
    a single Vibram Fivefingers shoe
    ---
    It's green and looks ridiculous. It's for the left foot.
    """
    shortname       = 'Single Vibram Shoe'
    adjectives      = 'green vibram fivefingers'
    nouns           = 'shoe'
    icon            = 'icon-hanger'
    # ---
    fits            = (EQ_PARTS.FEET,)

class MotorcycleHelmet(Equipable):
    """
    a tinted, black motorcycle helmet
    ---
    You might not die if you fell off a motorcycle while wearing this.
    """
    shortname       = 'Motorcycle Helmet'
    adjectives      = 'motorcycle'
    nouns           = 'helmet'
    icon            = 'icon-hanger'
    # ---
    fits            = (EQ_PARTS.HEAD,)

class CivilWarTrenchcoat(Equipable):
    """
    a blue civil war era trenchcoat
    ---
    Its blue and old.
    """
    shortname       = 'Civil War Trenchcoat'
    adjectives      = 'civil war trench blue'
    nouns           = 'trenchcoat coat'
    icon            = 'icon-tshirt'
    # ---
    fits            = (EQ_PARTS.SHOULDERS,)

# --- DEVICES --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Radio(Portable):
    """
    a small shortwave radio
    ---
    A small, battery operated, shortwave radio. This might be useful for communicating
    with other survivors.
    """
    attributes      = 'usable'
    shortname       = 'Radio'
    adjectives      = 'small shortwave'
    nouns           = 'radio'
    icon            = 'icon-radio'

    def use(self, other=None):
        raise TextyException('The radio emits a steady stream of static...')

class PowerMoves(Portable):
    """
    a copy of "Power Moves"
    ---
    D. Forsyth's autobiography. The book contains a number of powerful moves you can perform in
    various social and/or combat situations.
    """
    attributes      = 'usable'
    shortname       = 'Power Moves'
    adjectives      = ''
    nouns           = 'power moves book'
    icon            = 'icon-book2'

    def use(self, other=None):
        raise TextyException('You learn a new power move.')

# --- FOOD --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class ClifBar(Food):
    """
    an orginal Clif Bar&trade;
    ---
    The slick packaging makes you believe this is probably healthy for you. You consider a diet of
    only Clif Bars&trade;.
    """
    shortname       = 'Clif Bar&trade;'
    adjectives      = 'clif'
    nouns           = 'bar'
    icon            = 'icon-ticket'

class Burrito(Food):
    """
    a mission-style burrito
    ---
    It looks fucking delicious.
    """
    shortname       = 'Burrito'
    adjectives      = 'mission mission-style'
    nouns           = 'burrito'
    icon            = 'icon-food'

# --- CONTAINERS --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class Crate(Box):
    """
    a shockingly generic crate
    ---
    This is your standard videogame crate. Shockingly so. The texture looks really flat and it\'s
    just sitting there looking really generic and stuff.
    """
    shortname       = 'Crate'
    adjectives      = 'shockingly generic'
    nouns           = 'crate'
    icon            = 'icon-box2'
    # -- contents
    contents        = [Magazine9mm] * 5 + [Magazine45ACP] * 5 + [BoxRifleCartridges] * 5 + [Box12Gauge] * 5
