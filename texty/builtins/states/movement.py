"""
Various movement states
"""
class MovementState:

    def __init__(self, character):
        self.chatacter = character

    def enter(self):
        pass

    def exit(self, state, *args, **kwargs):
        return state(*args, **kwargs)

    def input(self, command):
        pass

    def on_attacked(self):
        pass

    def on_hurt(self, damage):

        if character.hitpoints <= -10:
            self.character.replace_stack(DeadState)

        elif character.hitpoints <= 0:
            self.character.replace_stack(OutState)



class StandingState(MovementState):

    def on_move(self):
        self.character.push_state(MovingState)

class MovingState(MovementState):

    def on_stop(self):
        self.character.pop_state()

    def on_spooked(self):
        self.character.pop_state()



class GroundedState(MovementState):
    pass
