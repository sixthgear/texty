"""
Information commands.
"""
from texty.engine.command import command, syntax, SCOPE, TextyException
from texty.util import serialize

@command('info')
def info(cmd, verb, object, prep, complement):
    cmd.to_source(str(cmd.source.nouns))
    return


@command('look', 'look at', 'examine')
def look(cmd, verb, object, prep, complement):
    """
    Look at things like a boss.
    """
    # command form D. VERB OBJECT PREP COMPLEMENT.
    if verb and object and complement and prep:
        raise TextyException("That doesn't make sense.")

    # command form C. VERB PREP OBJECT.
    elif verb and object and prep in ('in', 'into', 'inside'):
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(),                         "You don't see {x} here."),
            (lambda x,_: x.is_any('container ammo loadable'), "You can't look in {x}."),
            (lambda x,_: x.allows('look in'),                 "You can't look in {x}. {R}"),
            (lambda x,_: True,                                "You look inside {x}.")
        )
        cmd.response(msg)
        data = serialize.list(x.obj.contents, '{} is inside.')
        if not data['items']:
            data['items'] = [{'text': 'It\'s empty.'}]
        cmd.to_source(data)

        return

    # command form B. VERB OBJECT.
    elif verb and object and (not prep or prep == 'at'):
        valid, msg, x, _ = cmd.rules(
            (lambda x,_: x.resolve(SCOPE.ANY),          "You don't see {x} here."),
            (lambda x,_: x.allows('look'),              "You can't look at {x}. {R}"),
            (lambda x,_: True,                          "You examine {x}."),
        )
        cmd.response(msg)

        cmd.to_source({'type': 'object', 'items': [{'icon': x.obj.icon, 'text': x.obj.description}]})

        if x.is_any('ammo loadable'):
            data = serialize.list(x.obj.contents, '{} is inside.')
            if not data['items']:
                data['items'] = [{'text': 'It\'s empty.'}]
            cmd.to_source(data)

        if x.is_a('character'):
            cmd.to_source(serialize.list(x.obj.equipment, 'He is wearing {}.'))

        return

    # command form A. VERB.
    elif verb:
        cmd.response('You examine your surroundings.')
        cmd.to_source(serialize.room(cmd.room))
        cmd.to_source('X:Exits: {}'.format(', '.join([x.name for x in cmd.room.exits])))
        cmd.to_source(serialize.list(cmd.room.contents, '{} is here.', exclude=[cmd.source]))
        return

    raise TextyException("That doesn't make ANY sense.")

