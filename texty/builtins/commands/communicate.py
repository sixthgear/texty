"""
Communication commands.
"""
from texty.engine.command import command, syntax

# @syntax ("say DIALOUGE...")
# @syntax ("say DIALOUGE... [to] CHARACTER")
# @syntax ("say [to] CHARACTER DIALOUGE...")
@command  ("say", "shout", "ask", "tell", "ask", "\"")
def say(command, verb, object, prep, complement, string):
    """
    """

    if not string:
        return command.response('Say what?')
    string = string.replace('"', '').strip()
    command.to_source('C: <b>You say</b> "%s"' % string)
    command.to_room('C:<b>%s<b> says "%s"' % (command.source.name, string))
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


