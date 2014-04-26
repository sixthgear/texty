from collections import OrderedDict
from texty.util.enums import EQ_PARTS
from texty.util.english import resolve_single


class STRINGS:

    class LOOK:

        here        = "{Name} {is} {activity} here."
        inside      = "{Name} {is} inside."
        wearing     = "{You} {are} wearing {thing} on {your} {head}."
        holding     = "{You} {are} holding {thing} in {your} {hand}."
        inv         = "{You} {have} {thing}."

    class PERCIEVE:

        sense_near  = "{You} {sense} {thing} nearby!"
        sense_far   = "{You} {sense} {thing} in the distance."

    class HEALTH:

        bleed_1     = "{You} {are} bleeding."
        bleed_2     = "{You} {are} bleeding profusely from several wounds."
        bleed_part  = "{Your} {head} {is} bleeding."
        dizzy       = "{You} feel lightheaded."
        heart       = "{Your} heart is pounding."
        breath      = "{You} are gasping for air."

    class COMBAT:

        ammo        = "{He} {has} {amount} {rounds} remaining in your {weapon}."

        aim         = "{He} point{s} {his} {weapon} at {target} to {direction}."

        fire_1      = "{He} fire{s} {amount} {rounds} from {his} {weapon}."
        fire_2      = "{He} unleash{es} a hail of automatic gunfire!"

        swing       = "{He} swing{s} {his} {weapon} mercilessly at {target}."

        crit_1      = "{Targets} skull crumples under the weight of {your} powerful blow!"
        crit_2      = "{Target} was shot cleanly between the eyes!"
        crit_3      = "{Target} is cut to ribbons by {your} accurate firing! \
                       {Its} remaining body parts spill across the {ground}."
        crit_4      = "{Targets} head is neatly rendered from {its} shoulders and rolls away."

        hit_part_1  = "{Target} is {shot} in the {head}."
        hit_part_2  = "{Target} takes {num} {shots} to the {head}."

        result_1    = "{Target} crumple{s} to the ground gurgling and convulsing."
        result_2    = "{Target} is stunned for a moment, but continues to {approach} {you}!"




def dispatch(data):

    if isinstance(data, dict):
        return data

    if not isinstance(data, str):
        return {}

    # broadcast
    if data.startswith('B:'):
        data = {
            'type': 'broadcast',
            'text': data[2:]
        }
    # conversation
    elif data.startswith('C:'):
        data = {
            'type': 'conversation',
            'items': [ {'icon': 'fa-quote-left', 'text': data[2:]}, ]
        }
    # action
    elif data.startswith('A:'):
        data = {
            'type': 'action',
            'items': [ {'icon': 'fa-bolt', 'text': data[2:]}, ]
        }

    elif data.startswith('MV:'):
        data = {
            'type': 'action',
            'items': [ {'icon': 'icon-steps', 'text': data[3:]}, ]
        }
    # info
    elif data.startswith('I:'):
        data = {
            'type': 'info',
            'items': [ {'icon': 'icon-eye', 'text': data[2:]},]
        }
    elif data.startswith('X:'):
        data = {
            'type': 'info',
            'items': [ {'icon': 'icon-exit', 'text': data[2:]},]
        }
    # other
    else:
        data = {
            'type': 'action',
            'items': [ {'text': data} ]
        }

    return data


def room(room):
    """
    Serialize room data into a description.
    """
    data = {}
    data['type'] = 'description'
    data['intro'] = room.name
    data['text'] = room.description
    return data

def char(char, template='{} is here.'):
    """
    Serialize a character for brief mention.
    """
    data = {}
    data['icon'] = char.icon

    if char.activity:
        template = '{} is here'
        template += ' {}.'.format(char.activity)

    if char.occupation:
        job = char.occupation.lower()
        data['text'] = template.format('<b>{name}</b> the {job}'.format(name=char.first, job=job))
    else:
        data['text'] = template.format('<b>{name}</b>'.format(name=char.name))

    return data

def obj(obj, template='{} is here.'):
    """
    Serialize an object.
    """
    data = {}

    if hasattr(obj, 'amount') and obj.amount != 1:
        template = template.replace('is', 'are')

    data['icon'] = obj.icon
    data['text'] = template.format('<b>{name}</b>'.format(name=obj.name))
    return data

def list(container, template='{} is here', exclude=None):
    """
    Serialize an object list.
    """
    data = {'type': 'object'}
    data['items'] = []

    for x in container:
        if exclude and x in exclude: continue
        if x.is_a('character'):
            item = char(x, template)
        else:
            item = obj(x, template)
        data['items'].append(item)

    return data

def eq(character, source=None, exclude=None):
    """
    Serialize an object list.
    """
    data = {'type': 'object'}
    data['items'] = []

    for part, x in character.eq_map.items():

        if exclude and x in exclude: continue
        if not x: continue

        if part in (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND):
            template = resolve_single(character, '{He} is holding xx in {his} ', source).replace('xx', '{}')
            template += part.name.lower().replace('l_','left ').replace('r_','right ')
            template += '.'
        else:
            template = resolve_single(character, '{He} is wearing xx on {his} ', source).replace('xx', '{}')
            template += part.name.lower().replace('l_','left ').replace('r_','right ')
            template += '.'

        item = obj(x, template)
        data['items'].append(item)

    return data

def full_character(player):
    """
    Seriaize a full character update.
    """
    data = {'type': 'character'}

    status = [
        {'level': 'high', 'text': 'You feel cold,', 'icon': 'icon-temperature'},
        {'level': 'med', 'text': 'You feel hungry.', 'icon': 'icon-food'}
    ]

    inv = []
    for x in player.inventory:
        inv.append({
            'type': '',
            'name': x.shortname,
            'description': x.description,
            'icon': x.icon
        })

    eq = OrderedDict()
    for x, y in player.eq_map.items():
        slot = x.name.replace('_', '. ').title()
        item = y.shortname if y else '-'
        eq[slot] = item

    pack = {
        'name': '-',
        'capacity': 0,
        'amount': 0,
    }

    data['character'] = {
        'name': player.name,
        'occupation': player.occupation,
        'status': status,
        'inventory': inv,
        'equipment': eq,
        'pack': pack,
    }

    return data


