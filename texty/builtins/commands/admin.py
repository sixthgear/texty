from texty.engine.command import syntax, alias
from texty.builtins.story import Story

@syntax ("reset")
def reset(command):

    if not command.source.is_a('player'):
        return
    if not command.source.is_a('admin'):
        return

    command.response('Resetting game...')
    Story.get().clean()

