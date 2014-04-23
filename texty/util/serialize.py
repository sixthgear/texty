from collections import OrderedDict

def room(room):
    data = {}
    data['type'] = 'description'
    data['intro'] = room.title
    data['text'] = room.description
    return data

def obj(obj, template='{} is here.'):

    data = {}
    data['icon'] = obj.icon,
    data['text'] = template.format('<b>{name}</b>'.format(name=obj.name))
    return data

def list(container, template='{} is here', exclude=None):
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

def char(char, template='{} is here.'):
    """
    Turn character into a dict suitable for sending to client as JSON.
    """
    data = {}

    if char.gender in ('M', 'N'):
        data['icon'] = 'fa-male'
    elif char.gender == 'F':
        data['icon'] = 'fa-female'
    else:
        data['icon'] = ''

    if char.occupation:
        job = char.occupation.lower()
        data['text'] = template.format('<b>{name}</b> the {job}'.format(name=char.first, job=job))
    else:
        data['text'] = template.format('<b>{name}</b>'.format(name=char.name))

    return data


def full_character(player):
    """
    send full character update
    """
    data = {'type': 'character'}

    status = [
        {'level': 'high', 'text': 'You feel cold,', 'icon': 'fa-frown-o'},
        {'level': 'med', 'text': 'You feel hungry.', 'icon': 'fa-cutlery'}
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


