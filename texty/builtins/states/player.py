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

    def pop(self, *args, **kwargs):
        return self.character.pop_state()

    def push(self, state, *args, **kwargs):
        return self.character.push_state(state, *args, **kwargs)

    def replace(self, state, *args, **kwargs):
        return self.character.replace_stack(state, *args, **kwargs)

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self):
        pass

    def on_stop(self):
        pass

    def on_move(self, target, direction):
        self.push(MovingState, target=target, direction=direction)

    def on_hurt(self, damage):

        if self.character.hp <= -10:
            self.replace(DeadState)

        elif self.character.hp <= 0:
            self.replace(OutState)

        # large hits can knock out
        elif damage > 50:
            self.replace(OutState)



class RelaxedState(CharacterState):
    """
    Doing things which don't expect a fight. If the player is attacked when relaxed, they will
    be surprised.
    """

    def on_spooked(self):
        self.push(ReadyState)

    def on_ready(self):
        self.push(ReadyState)

    def on_target(self, target):
        self.push(ReadyState)
        self.push(FightingState, target=target)

    def on_attacked(self, target):
        self.push(ReadyState)
        self.push(FightingState, target=target)
        self.push(StunnedState, timer=2)


class MovingState(CharacterState):
    """
    Travelling from one node to the next. If attacked while moving, check to see if theres a
    ready or fighting state below.
    """

    def enter(self, target, direction):
        self.target = target
        self.direction = direction

    # already moving so change direction
    def on_move(self, target, direction):
        if direction != self.direction:
            self.target = target
            self.direction = direction

    def on_target(self, target):
        pass


    def on_attacked(self, target):
        # do different things depending on
        if len(self.character.state) > 1:

            # stop moving and attack aggressor after stunned penalty
            if isinstance(self.character.state[-2], (RelaxedState,)):
                self.pop()
                self.push(ReadyState)
                self.push(FightingState, target=target)
                self.push(StunnedState, timer=2)

            # stop moving and attack aggressor
            elif isinstance(self.character.state[-2], (ReadyState,)):
                self.pop()
                self.push(FightingState, target=target)

            # keep moving
            elif isinstance(self.character.state[-2], (Fighting,)):
                pass

    def on_stop(self):
        self.pop()

    # every tick continue movement
    def update(self):

        self.character.node.move_dir(self.character, self.direction)

        if self.character.node == self.target:
            self.character.stop()
            self.character.do('look')



class ReadyState(CharacterState):
    """
    Ready for a fight! Target is optional, but player can't be surprised by an attack.
    Auto-engage in-range hostiles.
    """
    max_timer = 30

    # reset idle timer whenever we reenter this state
    def enter(self, target=None):
        self.idle_timer = self.max_timer
        self.target = target

    def on_target(self, target):
        self.push(FightingState, target=target)

    # respond instantly if attacked in ready state
    def on_attacked(self, target):
        self.push(FightingState, target=target)

    # hit by a stunning blow
    def on_stunned(self, target):
        self.push(FightingState, target=target)
        self.push(StunnedState, timer=2)

    def update(self):
        self.idle_timer -= 1
        if self.idle_timer <= 0:
            return self.pop()


class FightingState(CharacterState):
    """
    Engaged in mortal combat.
    """

    def enter(self, target):

        # invalid state if no weapon available
        if not self.character.weapon or not self.character.weapon.loaded:
            return self.pop()

        self.target = target
        self.cooldown_timer = self.character.weapon.cooldown
        target.register('death', self.on_target_death)

    def exit(self):
        pass

    def on_target_death(self, target):
        self.pop()

    def on_stop(self):
        self.pop()

    def on_target(self, target):
        self.target = target

    def on_untarget(self):
        self.pop()

    def on_stunned(self):
        self.push(StunnedState, timer=2)

    def on_grappled(self, character):
        self.push(GrapplingState)

    def on_weapon_empty(self, weapon):
        self.pop(self.target)

    def update(self):

        self.cooldown_timer -= 1
        # perform combat tick
        if self.cooldown_timer <= 0:
            self.cooldown_timer = self.character.weapon.cooldown
            self.character.attack(self.target)


class GrapplingState(CharacterState):
    """
    Fighting hand-to-hand. Movement is restricted.
    """

    def on_released(self):
        self.pop()

    # may not move while grappling
    def on_move(self, target, direction):
        pass # nope.


class StunnedState(CharacterState):
    """
    When the character gets hit by a heavy blow they may become stunned. This state prevents
    movement, combat and interaction until the timer has expired.
    """
    max_timer = 2

    def enter(self, timer=None):
        self.timer = timer or self.max_timer

    # may not move while stunned
    def on_move(self, target, direction):
        pass

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.pop()


class OutState(CharacterState):
    """
    Knocked out.
    """
    max_timer = 30

    def enter(self):
        self.character.fall()
        self.timer = self.max_timer

    # may not move while knocked out
    def on_move(self, target, direction):
        pass

    def on_hurt(self, damage):

        if self.character.hp <= -10:
            self.replace(DeadState)

    def on_heal(self, hp):
        self.replace(RelaxedState)

    def on_revive(self, character):
        self.replace(RelaxedState)

    def on_stunned(self, character):
        self.replace(RelaxedState)

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            return self.pop()


class DeadState(CharacterState):
    """
    RIP
    """
    def enter(self):
        self.character.die()

    def on_hurt(self, damage):
        pass

    # may not move while dead
    def on_move(self, target, direction):
        pass
