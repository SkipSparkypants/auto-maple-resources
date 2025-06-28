"""A collection of all commands that a Bishop can use to interact with the game."""

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
        self.benediction_cast_time = 0
        self.door_cast_time = 0
        self.genesis_cast_time = 0
        self.peacemaker_cast_time = 0
        self.divine_punishment_cast_time = 0
        self.erda_shower_cast_time = 0
        self.heal_cast_time = 0
        self.infinity_cast_time = 0
        self.infinity_cast_time_2 = 0
        self.dispel_cast_time = 0
        self.epic_adventure_cast_time = 0
        self.bahamut_cast_time = 0
        self.snail_cast_time = 0
        self.blood_of_the_divine_cast_time = 0
        self.spider_cast_time = 0
        self.familiar_cast_time = 0

# List of key mappings
class Key:
    # Movement
    JUMP = 'space'
    TELEPORT = 'shift'

    # Buffs
    # 10
    HEAL = 'q'

    # 60
    DISPEL = 'f3'

    # 120
    EPIC_ADVENTURE = 'f2'

    # 180
    INFINITY = '`'
    INFINITY_2 = '1'
    BAHAMUT = 'r'
    SNAIL = '0'
    SPEED_INFUSION = 'f4'
    SHARP_EYES = 'f5'
    COMBAT_ORDERS = 'f6'

    # 240
    MACRO_BUFF = 'f1'
    ERDA_NOVA = 'v'

    # 260
    BLOOD_OF_THE_DIVINE = 'y'

    # 300
    RES = '4'

    # Skills
    ANGEL_RAY = 'a'
    FOUNTAIN = 'w'
    MAGIC_SHELL = '3'
    DIVINE_PUNISHMENT = 's'
    DOOR = 'f'
    BIG_BANG = 'd'
    GENESIS = '2'
    PEACEMAKER = 't'
    BENEDICTION = 'e'
    SOL_JANUS = 'l'
    ERDA_SHOWER = '8'
    SPIDER = '9'

    FAMILIAR = '-'

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
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 3)
            time.sleep(0.1)
        elif direction == 'up':
            press(Key.JUMP, 1)
            time.sleep(0.1)
    press(Key.BIG_BANG, 2, up_time=0.05)
    time.sleep(0.1)
    press(Key.TELEPORT, num_presses)
    if last_pos == config.player_pos:
        press(Key.JUMP, num_presses)
        press(Key.BIG_BANG, 2, up_time=0.05)
        press(Key.TELEPORT, 1)


def command_with_cooldown(cmd, now, cast_time, cooldown, down_time=0.2, times=3):
    if cast_time == 0 or now - cast_time > cooldown:
        press(cmd, times, down_time=down_time, up_time=0.05)
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
        self.timers = Timers()

    def main(self):
        for _ in range(2):
            now = time.time()
            # if command_with_cooldown(Key.HEAL, now, self.timers.heal_cast_time, 10):
            #     self.timers.heal_cast_time = now
            #     continue

            if command_with_cooldown(Key.DISPEL, now, self.timers.dispel_cast_time, 60):
                self.timers.dispel_cast_time = now
                continue

            if command_with_cooldown(Key.EPIC_ADVENTURE, now, self.timers.epic_adventure_cast_time, 120):
                self.timers.epic_adventure_cast_time = now
                continue

            if command_with_cooldown(Key.BAHAMUT, now, self.timers.bahamut_cast_time, 180):
                self.timers.bahamut_cast_time = now
                continue

            if command_with_cooldown(Key.SNAIL, now, self.timers.snail_cast_time, 180):
                self.timers.snail_cast_time = now
                continue

            if command_with_cooldown(Key.BLOOD_OF_THE_DIVINE, now, self.timers.blood_of_the_divine_cast_time, 260):
                self.timers.blood_of_the_divine_cast_time = now
                continue

            if command_with_cooldown(Key.FAMILIAR, now, self.timers.familiar_cast_time, 3600, times=1):
                self.timers.familiar_cast_time = now
                continue

            if command_with_cooldown(Key.INFINITY, now, self.timers.infinity_cast_time, 180, down_time=0.2):
                self.timers.infinity_cast_time = now
                continue
            elif (now - self.timers.infinity_cast_time > 120) and command_with_cooldown(Key.INFINITY_2, now, self.timers.infinity_cast_time_2, 180, down_time=0.2):
                self.timers.infinity_cast_time_2 = now
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
        num_presses = 2
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
                press(Key.JUMP, 2)
        if self.direction == 'up':
            key_down(self.direction)
            time.sleep(0.05)
        press(Key.BIG_BANG, 2, up_time=0.05)
        press(Key.TELEPORT, num_presses)
        key_up(self.direction)
        if settings.record_layout:
            config.layout.add(*config.player_pos)

class Attack(Command):
    """Attacks using in a given direction."""
    def __init__(self, attacks=1):
        super().__init__(locals())
        self.attacks = int(attacks)
        self.angel_ray = AngelRay()
        self.timers = Timers()

    def main(self):
        for _ in range(self.attacks):
            now = time.time()
            if command_with_cooldown(Key.BENEDICTION, now, self.timers.benediction_cast_time, 180):
                self.timers.benediction_cast_time = now
                continue
            if command_with_cooldown(Key.DOOR, now, self.timers.door_cast_time, 60):
                self.timers.door_cast_time = now
                continue
            if command_with_cooldown(Key.GENESIS, now, self.timers.genesis_cast_time, 30):
                self.timers.genesis_cast_time = now
                continue
            if command_with_cooldown(Key.PEACEMAKER, now, self.timers.peacemaker_cast_time, 10):
                self.timers.peacemaker_cast_time = now
                continue
            # if command_with_cooldown(Key.DIVINE_PUNISHMENT, now, self.timers.divine_punishment_cast_time, 34, 2, 1):
            #     self.timers.divine_punishment_cast_time = now
            #     continue
            if command_with_cooldown(Key.ERDA_SHOWER, now, self.timers.erda_shower_cast_time, 60):
                self.timers.erda_shower_cast_time = now
                continue
            if command_with_cooldown(Key.SPIDER, now, self.timers.spider_cast_time, 250):
                self.timers.spider_cast_time = now
                continue

        # press(Key.BIG_BANG, 2)

class AngelRay(Command):

    """Uses 'AngelRay' once."""
    def main(self):
        press(Key.ANGEL_RAY, 5)
        return True

class Fountain(Command):
    """
    Places 'Fountain' in a given direction, or towards the center of the map if
    no direction is specified.
    """

    def __init__(self, direction=None):
        super().__init__(locals())
        if direction is None:
            self.direction = direction
        else:
            self.direction = settings.validate_horizontal_arrows(direction)

    def main(self):
        numPresses = 1
        down_time = 0.3
        up_time = 0.05
        if self.direction:
            press(self.direction, numPresses, down_time=down_time, up_time=up_time)
        else:
            if config.player_pos[0] > 0.5:
                press('left', numPresses, down_time=down_time, up_time=up_time)
            else:
                press('right', numPresses, down_time=down_time, up_time=up_time)
        press(Key.FOUNTAIN, 2)

class SolJanus(Command):
    """
    Places 'Sol Janus'.
    """

    def main(self):
        press(Key.SOL_JANUS, 2)


class Def(Command):
    """Uses each of Bishop's buffs once. Uses 'Haku Reborn' whenever it is available."""

    def __init__(self):
        super().__init__(locals())
        
    def main(self):
        press(Key.MAGIC_SHELL, 1, down_time=0.2)
