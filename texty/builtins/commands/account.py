from texty.builtins.story import Story

def hello(command):
    Story.get().login_prompt(command.source)
    return

def login(command):
    # TODO: perform authentication
    if len(command.arguments) == 0:
        command.to_source('Login as who?')
        return

    name = command.arguments[0]
    command.source.name = name
    command.source.keywords = [name.lower()]
    get_story().begin(command.source)
    return
