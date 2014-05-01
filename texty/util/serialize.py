from collections import OrderedDict
from texty.util.enums import EQ_PARTS
from texty.util.english import STR
from texty.util.parsertools import lookahead
import re
"""
Tools for producing JSON serializable dicts for sending to the client.
"""

def dispatch(data):

    shortcuts = {
        'M:':  ('action', 'icon-steps'),
        'A:':  ('action', 'fa-bolt'),
        'C:':  ('conversation', 'fa-quote-left'),
        'I:':  ('info', 'icon-eye'),
        'X:':  ('info', 'icon-exit'),
    }

    if isinstance(data, dict):
        return data

    if not data or not isinstance(data, str):
        return {}

    new = {}

    # list
    if data.startswith(tuple(shortcuts)):
        new['type'], icon = shortcuts[data[:2]]
        new['items'] = [{'icon': icon, 'text': data[2:]}]

    # broadcast
    elif data.startswith('B:'):
        new['type'] = 'broadcast'
        new['text'] = data[2:]

    else:
        new['type'] = 'action'
        new['items'] = [{'icon': '', 'text': data[2:]}]

    return new


def node(node):
    """
    Serialize node data into a description.
    """
    data = {}
    data['type'] = 'description'
    data['intro'] = node.name
    data['text'] = node.description or node.nearby
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
        data['text'] = template.format(sub=obj, **{'is': 'are'})
        data['icon'] = obj.icon
    else:
        data['text'] = template.format(sub=obj, **{'is': 'is'})
        data['icon'] = obj.icon

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


def vislist(nearby, template=STR.INFO.here_dist, exclude=None):
    """
    Serialize a visible object list.
    """
    data = {'type': 'object'}
    data['items'] = []

    combined = []

    for obj, next_obj in lookahead(nearby):

        x, dist, dir = obj

        if exclude and x in exclude: continue

        if next_obj:
            next_x, next_dist, next_dir = next_obj
            if x.is_a('monster') and dist > 0 and dist == next_dist and dir == next_dir and x.__class__ == next_x.__class__:
                combined += [obj]
                continue

        if combined:
            dir = dir.name.lower()
            dist = str(dist*10)+'m'
            item = {}
            item['icon'] = x.icon
            item['text'] = STR.T(STR.INFO.here_many, x, extra={'num': len(combined)+1, 'dist': dist, 'dir': dir})
            combined = []

        elif dist == 0 and x.is_a('character'):
            item = char(x, STR.INFO.here)
        elif dist == 0:
            item = obj(x, STR.INFO.here)
        elif x.is_a('character'):
            dir = dir.name.lower()
            dist = str(dist*10)+'m'
            item = {}
            item['icon'] = x.icon
            item['text'] = STR.T(template, x, extra={'are': 'is', 'dist': dist, 'dir': dir})
        else:
            dir = dir.name.lower()
            dist = str(dist*10)+'m'
            item = {}
            item['icon'] = x.icon
            item['text'] = template.format(sub=x, **{'is': 'is', 'dist': dist, 'dir': dir})

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


