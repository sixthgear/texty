"""
Information commands.
"""
from texty.engine.command import command, syntax, SCOPE, TextyException
from texty.util import serialize
from texty.util.english import STR

@command('info')
def info(cmd, verb, object, prep, complement):
    for s in cmd.source.state:
        cmd.to_source('I:' + s.__class__.__name__)
    return


@command('look', 'look at', 'examine', "l")
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
        data = serialize.list(x.obj.contents, STR.INFO.inside)
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
            data = serialize.list(x.obj.contents, STR.INFO.inside)
            if not data['items']:
                data['items'] = [{'text': 'It\'s empty.'}]
            cmd.to_source(data)

        if x.is_a('character'):
            cmd.to_source(serialize.eq(x.obj, source=cmd.source))

        return

    # command form A. VERB.
    elif verb:
        cmd.response('You examine your surroundings.')
        cmd.to_source(serialize.node(cmd.node))
        cmd.to_source('X:Exits: {}'.format(', '.join([x.name for x in cmd.node.exits])))
        # int=cmd.node.interval[cmd.source]
        # objs = [o[0] for o in ]
        cmd.to_source(serialize.vislist(cmd.node.visible(10, character=cmd.source), STR.INFO.here_dist, exclude=[cmd.source]))
        cmd.to_source(serialize.list(cmd.node.objects, STR.INFO.here, exclude=[cmd.source]))

        return

    raise TextyException("That doesn't make ANY sense.")

