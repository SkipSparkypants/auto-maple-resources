"""A collection of all commands that a Hero can use to interact with the game."""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up


class Timers(Command):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Timers, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__(locals())
        self.whirlpool_cast_time = 0
        self.striking_tide_cast_time = 0
        self.water_wheel_cast_time = 0
        self.thunder_clap_cast_time = 0
        self.waterfall_cast_time = 0

# List of key mappings
class Key:
    # Movement
    JUMP = 'space'
    TELEPORT = 'shift'

    # Buffs
    # 10

    # 60

    # 120

    # 180
    WARRIOR = '`'

    # 240

    # 260

    # 300

    # Skills
    BASIC_SWORD = 'q'
    WHIRLPOOL = 'w'
    STRIKING_TIDE = 'e'
    WATER_WHEEL = 'r'
    THUNDER_CLAP = 't'
    WATERFALL = '1'

#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    num_presses = 2
    last_pos = config.player_pos
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 3)
            time.sleep(0.15)
            press(Key.TELEPORT, num_presses)
        elif direction == 'up':
            press(Key.JUMP, 1)
    if last_pos == config.player_pos:
        press(Key.JUMP, num_presses)


def command_with_cooldown(cmd, now, cast_time, cooldown, down_time=0.2, times=3):
    if cast_time == 0 or now - cast_time > cooldown:
        press(cmd, times, down_time=down_time)
        return True
    return False


class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        key_down('left')
                        while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        Teleport('up').main()
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 3, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Bishop's buffs when available."""

    def __init__(self):
        super().__init__(locals())
        self.buff_time = 0
        self.buff_time_10 = 0
        self.buff_time_60 = 0
        self.buff_time_120 = 0
        self.buff_time_240 = 0
        self.buff_time_260 = 0
        self.buff_time_300 = 0
        self.buffs = [Key.WARRIOR]

    def main(self):
        now = time.time()
        for _ in range(2):
            if self.buff_time_10 == 0 or now - self.buff_time_10 > 10:

                self.buff_time_10 = now
                continue

            if self.buff_time_60 == 0 or now - self.buff_time_60 > 60:
                self.buff_time_60 = now
                continue

            if self.buff_time_120 == 0 or now - self.buff_time_120 > 120:
                self.buff_time_120 = now
                continue

            if self.buff_time == 0 or now - self.buff_time > settings.buff_cooldown: # 180
                for key in self.buffs:
                    press(key, 1, down_time=0.8, up_time=0.1)
                self.buff_time = now
                continue

            if self.buff_time_240 == 0 or now - self.buff_time_240 > 240:
                self.buff_time_240 = now
                continue

            if self.buff_time_260 == 0 or now - self.buff_time_260 > 260:
                self.buff_time_260 = now
                continue

            if self.buff_time_300 == 0 or now - self.buff_time_240 > 300:
                self.buff_time_300 = now
                continue

class Teleport(Command):
    """
    Teleports in a given direction, jumping if specified. Adds the player's position
    to the current Layout if necessary.
    """

    def __init__(self, direction, jump='False'):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)
        self.jump = settings.validate_boolean(jump)

    def main(self):
        num_presses = 3
        time.sleep(0.05)
        if self.direction in ['up', 'down']:
            num_presses = 2
        if self.direction != 'up':
            key_down(self.direction)
            time.sleep(0.05)
        if self.jump:
            if self.direction == 'down':
                press(Key.JUMP, 3, down_time=0.1)
            else:
                press(Key.JUMP, 1)
        if self.direction == 'up':
            key_down(self.direction)
            time.sleep(0.05)
            press(Key.TELEPORT, num_presses)
        key_up(self.direction)
        if settings.record_layout:
            config.layout.add(*config.player_pos)

class Attack(Command):
    """Attacks using in a given direction."""
    def __init__(self, attacks=2):
        super().__init__(locals())
        self.attacks = int(attacks)
        self.timers = Timers()

    def main(self):
        now = time.time()
        command_with_cooldown(Key.BASIC_SWORD, now, 0.5, 0)

        for _ in range(self.attacks):
            if command_with_cooldown(Key.WATER_WHEEL, now, self.timers.water_wheel_cast_time, 4):
                self.timers.water_wheel_cast_time = now
                continue
            if command_with_cooldown(Key.WHIRLPOOL, now, self.timers.whirlpool_cast_time, 7):
                self.timers.whirlpool_cast_time = now
                continue
            if command_with_cooldown(Key.WATERFALL, now, self.timers.waterfall_cast_time, 10):
                self.timers.waterfall_cast_time = now
                continue
            if command_with_cooldown(Key.STRIKING_TIDE, now, self.timers.striking_tide_cast_time, 120):
                self.timers.striking_tide_cast_time = now
                continue
            if command_with_cooldown(Key.THUNDER_CLAP, now, self.timers.thunder_clap_cast_time, 180):
                self.timers.thunder_clap_cast_time = now
                continue

class Def(Command):
    """Uses each of Bishop's buffs once. Uses 'Haku Reborn' whenever it is available."""

    def __init__(self):
        super().__init__(locals())

    def main(self):
        return None
