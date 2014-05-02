"""
Various movement and combat states
"""
# from texty.builtins.states.movement import MovingState

class CharacterState:
    """
    Base state that defines transitions that can take place in any stack configuration.
    """

    def __init__(self, character):
        self.character = character

    def enter(self):
        pass

    def exit(self):
        pass

    def input(self, command):
        pass

    def update(self):
        pass

    def on_stop(self):
        pass

    def on_move(self):
        self.character.push_state(MovingState)

    def on_hurt(self, damage, kind):

        if character.hitpoints <= -10:
            self.character.replace_stack(DeadState)

        elif character.hitpoints <= 0:
            self.character.replace_stack(OutState)

        # large hits can knock out
        elif damage > 50:
            self.character.replace_stack(OutState)



class RelaxedState(CharacterState):
    """
    Doing things which don't expect a fight. If the player is attacked when relaxed, they will
    be surprised.
    """

    def on_spooked(self):
        self.character.push_state(ReadyState)

    def on_ready(self):
        self.character.push_state(ReadyState)

    def on_attack(self, character):
        self.character.push_state(ReadyState)
        self.character.push_state(FightingState, target=character)

    def on_attacked(self, character):
        self.character.push_state(ReadyState)
        self.character.push_state(FightingState, target=character)
        self.character.push_state(StunnedState, timer=2)


class MovingState(CharacterState):
    """
    Travelling from one node to the next. If attacked while moving, check to see if theres a
    ready or fighting state below.
    """

    def enter(self):
        pass

    # already moving so do nothing
    def on_move(self):
        pass
        # self.character.push_state(MovingState)

    def on_attacked(self, character):

        if len(self.character.state) > 1:

            # stop moving and attack aggressor after stunned penalty
            if isinstance(self.character.state[-2], (RelaxedState,)):
                self.character.pop_state()
                self.character.push_state(ReadyState)
                self.character.push_state(FightingState, target=character)
                self.character.push_state(StunnedState, timer=2)

            # stop moving and attack aggressor
            elif isinstance(self.character.state[-2], (ReadyState,)):
                self.character.pop_state()
                self.character.push_state(FightingState, target=character)

            # keep moving
            elif isinstance(self.character.state[-2], (Fighting,)):
                pass

    def on_stop(self):
        self.character.pop_state()

    # every tick continue movement
    def update(self):

        self.character.move_continue()

        if self.character.move_target == self.character.node:
            self.character.stop()
            self.character.do('look')



class ReadyState(CharacterState):
    """
    Ready for a fight! Target is optional, but player can't be surprised by an attack.
    Auto-engage in-range hostiles.
    """
    max_timer = 30

    def enter(self):
        self.timer = max_timer

    def on_attack(self, character):
        self.character.push_state(FightingState, target=character)

    def on_attacked(self, character):
        self.character.push_state(FightingState, target=character)

    def on_stunned(self, character):
        self.character.push_state(FightingState, target=character)
        self.character.push_state(StunnedState, timer=2)

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            return self.character.pop_state()


class FightingState(CharacterState):
    """
    Engaged in mortal combat.
    """

    def enter(self, target):
        pass

    def on_stunned(self):
        self.character.push_state(StunnedState, timer=2)

    def on_grappled(self, character):
        self.character.push_state(GrapplingState)

    def update(self):
        # perform combat tick
        self.character.combat()


class GrapplingState(CharacterState):
    """
    Fighting hand-to-hand. Movement is restricted.
    """

    def on_released(self):
        self.character.pop_state()

    # may not move while grappling
    def on_move(self):
        pass # nope.


class StunnedState(CharacterState):
    """
    When the character gets hit by a heavy blow they may become stunned. This state prevents
    movement, combat and interaction until the timer has expired.
    """
    max_timer = 2

    def enter(self):
        self.timer = max_timer

    # may not move while stunned
    def on_move(self):
        pass

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.character.pop_state()


class OutState(CharacterState):
    """
    Knocked out.
    """
    max_timer = 30

    def enter(self):
        self.timer = max_timer

    # may not move while knocked out
    def on_move(self): # nope.
        pass

    def on_hurt(self, damage):
        if character.hitpoints <= -10:
            self.character.replace_stack(DeadState)

    def on_heal(self, hp):
        self.character.replace_stack(RelaxedState)

    def on_revive(self, character):
        self.character.replace_stack(RelaxedState)

    def on_stunned(self, character):
        self.character.replace_stack(RelaxedState)

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            return self.character.pop_state()


class DeadState(CharacterState):
    """
    RIP
    """
    def on_hurt(self, damage):
        pass

    # may not move while dead
    def on_move(self): # nope.
        pass
