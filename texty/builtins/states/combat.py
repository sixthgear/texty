"""
Various combat states
"""
from texty.builtins.states.movement import MovingState

class CombatState:

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



class RelaxedState(CombatState):
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


class MovingState(CombatState):

    def enter(self):
        pass

    def on_stop(self):
        self.character.pop_state()

    def update(self):
        self.character.move_continue()
        if self.character.move_target == self.character.node:
            self.character.stop()
            self.character.do('look')



class ReadyState(CombatState):
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


class FightingState(CombatState):
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


class GrapplingState(CombatState):
    """
    Fighting hand-to-hand. Movement is restricted.
    """

    def on_released(self):
        self.character.pop_state()

    def on_move(self):
        pass # nope.


class StunnedState(CombatState):
    """
    When the character gets hit by a heavy blow they may become stunned. This state prevents
    movement, combat and interaction until the timer has expired.
    """
    max_timer = 2

    def enter(self):
        self.timer = max_timer

    def on_move(self): # nope.
        pass

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.character.pop_state()


class OutState(CombatState):
    """
    Knocked out.
    """
    max_timer = 30

    def enter(self):
        self.timer = max_timer

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


class DeadState(CombatState):
    """
    RIP
    """
    def on_hurt(self, damage):
        pass


