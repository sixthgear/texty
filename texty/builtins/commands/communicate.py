"""
Communication commands.
"""

from texty.engine.command import syntax, alias

@syntax ("say DIALOUGE...")
@syntax ("say DIALOUGE... [to] CHARACTER")
@syntax ("say [to] CHARACTER DIALOUGE...")
@alias  ("shout", "ask", "tell", "ask", "\"")
def say(command):
    """
    """
    if len(command.arguments) == 0:
        return command.response('Say what?')
    message = ' '.join(command.arguments)
    command.to_source('You say <span class="dialouge me">"%s"</span>' % message)
    command.to_room('%s says <span class="dialouge">"%s"</span>' % (command.source, message))
    return


def emote(command):
    """
    """
    pass

def follow(command):
    """
    """
    pass

def party(command):
    """
    party
    """
    pass

def invite(command):
    """
    """
    pass

def join(command):
    """
    """
    pass


@syntax ("trade")
@syntax ("trade [with,to] CHARACTER")
@syntax ("trade I.PORTABLE...")
@syntax ("trade I.PORTABLE... [with,to] CHARACTER")
@alias  ("offer", "barter")
def trade(command):
    """
    """
    pass


