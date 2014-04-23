"""
Information commands.
"""
from texty.engine.command import command, syntax, SCOPE, TextyException


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
            (lambda x,_: x.resolve(),                    "You don't see {x} here."),
            (lambda x,_: x.is_any('container ammo'),     "You can't look in {x}."),
            (lambda x,_: x.allows('look in'),            "You can't look in {x}. {R}"),
            (lambda x,_: True,                           "You look inside {x}.")
        )
        cmd.response(msg)
        cmd.to_source(x.obj.serialize_contents())
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

        if x.is_any('container ammo'):
            cmd.to_source(x.obj.serialize_contents())
        return

    # command form A. VERB.
    elif verb:
        cmd.response('You examine your surroundings.')
        cmd.to_source(cmd.room.serialize())
        cmd.to_source('I:Exits: {}'.format(" ".join([x.upper() for x in cmd.room.exits.keys()])))
        cmd.to_source({
            'type': 'object',
            'items': [o.serialize() for o in cmd.room.contents if o != cmd.source]})
        return

    raise TextyException("That doesn't make ANY sense.")

