from texty.engine.command import command, syntax
from texty.builtins.story import Story

@command ("rrreset")
def reset(command, verb, object, prep, complement):

    if not command.source.is_a('player'):
        return
    # if not command.source.is_a('admin'):
    #     return

    command.response('Resetting game...')
    Story.get().clean()

