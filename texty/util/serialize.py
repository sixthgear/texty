from collections import OrderedDict
from texty.util.enums import EQ_PARTS
from texty.util.english import STR
"""
Tools for producing JSON serializable dicts for sending to the client.
"""

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

def char(char, template=STR.INFO.here):
    """
    Serialize a character for brief mention.
    """
    data = {}
    data['icon'] = char.icon
    data['text'] = STR.T(template, char, extra={'are': 'is'})
    return data

def obj(obj, template=STR.INFO.here):
    """
    Serialize an object.
    """
    data = {}
    if hasattr(obj, 'plural') and obj.plural:
        are = 'are'
    else:
        are = 'is'

    data['icon'] = obj.icon
    data['text'] = template.format(sub=obj, are=are)
    return data

def list(container, template=STR.INFO.here, exclude=None):
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
    Serialize an equipment list
    """
    data = {'type': 'object'}
    data['items'] = []

    for part, x in character.eq_map.items():

        if exclude and x in exclude: continue
        if not x: continue

        if part in (EQ_PARTS.L_HAND, EQ_PARTS.R_HAND):
            template = STR.INFO.holding
        else:
            template = STR.INFO.wearing

        part = part.name.lower().replace('l_', 'left ').replace('r_', 'right ')
        text = STR.T(template, character, source=source, extra={'x': x, 'y':part})
        item = obj(x, text)
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


