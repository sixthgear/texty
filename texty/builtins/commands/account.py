from texty.engine.story import Story

def hello(command, verb, object, prep, complement):
    Story.get().login_prompt(command.source)
    return

def login(command, verb, object, prep, complement):
    # TODO: perform authentication
    if len(command.arguments) == 0:
        command.to_source('Login as who?')
        return

    name = command.arguments[0]
    command.source.name = name
    command.source.keywords = [name.lower()]
    get_story().begin(command.source)
    return
