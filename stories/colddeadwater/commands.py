from texty.engine.command import command, syntax
from texty.builtins.story import Story

@command ("wakeup")
def wakeup(command, verb, object, prep, complement):

    if not command.source.is_a('player'):
        return

    p = command.source
    p.move_to(Story.get().starting_room)

    command.to_room(
        'A:The door opens suddenly and <b>%s</b> the %s is tossed onto a bed in the corner. \
        <span class="sound-2x">&mdash;WHUMP&mdash;</span>' % (p.name, p.occupation))

    p.send('I:"Yes, %s." you remember.' % p.name)
    p.send('C:"%s? %s?", <b>a voice echoes in the distance.</b>' % (p.first, p.first))
    p.send('C:"%s?!"' % p.first)
    p.send('A:You are violently jolted back into reality. \
        A wiry figure is shaking your shoulders with thin, bony fingers.')
    p.send('C:"%s, you\'re alright! One of the patrols found you face down in the mud. \
        They were sure you were dead at first, but they picked you up and brought you back here. \
        I\'m glad you made it."' % p.first)
    p.send('I:"Bertram", you think to yourself. "I remember him."')


@command ("combust")
def combust(command, verb, object, prep, complement):

    if not command.source.is_a('player'):
        return

    p = command.source
    command.to_room(
        'A:Suddenly, %s bursts into flames! \
        <span class="sound-3x">AAAAAAAUUUUGHHH!!</span> \
        In a few moments nothing is left of %s but ashes \
        and a few flecks of charred bone.' % (p.name, p.first))

    p.move_to(None)
