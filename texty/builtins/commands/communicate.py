"""
Communication commands.
"""
from texty.engine.command import command, syntax

# @syntax ("say DIALOUGE...")
# @syntax ("say DIALOUGE... [to] CHARACTER")
# @syntax ("say [to] CHARACTER DIALOUGE...")
@command  ("say", "shout", "ask", "tell", "ask", "\"")
def say(command, verb, object, prep, complement):
    """
    """
    if len(command.arguments) == 0:
        return command.response('Say what?')
    message = ' '.join(command.arguments)
    command.to_source('You say <span class="dialouge me">"%s"</span>' % message)
    command.to_room('%s says <span class="dialouge">"%s"</span>' % (command.source, message))
    return


def emote(command, verb, object, prep, complement):
    """
    """
    pass

def follow(command, verb, object, prep, complement):
    """
    """
    pass

def party(command, verb, object, prep, complement):
    """
    party
    """
    pass

def invite(command, verb, object, prep, complement):
    """
    """
    pass

def join(command, verb, object, prep, complement):
    """
    """
    pass


@syntax ("trade")
@syntax ("trade [with,to] CHARACTER")
@syntax ("trade I.PORTABLE...")
@syntax ("trade I.PORTABLE... [with,to] CHARACTER")
@command  ("trade" ,"offer", "barter")
def trade(command, verb, object, prep, complement):
    """
    """
    pass


