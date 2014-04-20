"""
Information commands.
"""
from texty.engine.command import command, syntax

@command('look',  'examine')
def look(command, verb, object, prep, complement):

    # resolve objects
    if complement:
        if prep in ('with', 'using'):
            return
        return command.response('That doesn\'t make sense.')

    elif prep:
        if prep in ('in', 'inside', 'into'):
            obj = command.resolve(object, scope='IN')
        elif prep == 'at':
            obj = command.resolve(object)
        else:
            return command.response('You can\'t look <b>%s</b> something.' % prep)

    elif object:
        obj = command.resolve(object)

    else:
        obj = command.room

    if not obj:
        # resolution failed
        n = object['noun']
        a = object.get('indef') or object.get('spec') or 'a'
        return command.response('You don\'t see {} {} here.'.format(a, n))

    elif obj == command.room:
        # look at room
        command.response('You examine your surroundings.')
        command.to_source(obj.serialize())
        command.to_source({
            'type': 'object',
            'items': [o.serialize() for o in obj.contents if o != command.source]
        })
        return

    # return the description of the object
    command.response('You examine %s.' % obj.name)
    command.to_source({'type': 'object', 'items': [{'icon': obj.icon, 'text': obj.description}]})
    return



