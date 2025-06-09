"""A collection of all commands that Shadower can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from src.common.vkeys import press, key_down, key_up


# List of key mappings
class Key:
    # Movement
    JUMP = 'f'
    FLASH_JUMP = 'f'

    # Buffs
    SHADOW_ILLUSION = 'r'
    SHADOW_SPEAR = '1'
    GREATER_SERVANT = '4'
    ERDA_SHOWER = '8'
    CYGNUS = '3'
    FINAL = '5'

    # Origin
    ORIGIN = 'w'

    # Skills
    RAPID_THROW = 'd'
    SHADOWBITE = 'q'
    DARKOMEN = 'alt'
    QUADSTAR = 'a'
    SHADOW_SPARK = 'g'
    DOMINION = 'e'
    JANUS = '9'




#########################
#       Commands        #
#########################

class Timers(Command):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Timers, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__(locals())
        self.shadow_illusion = 0
        self.Shadow_spear = 0
        self.Greater_servant = 0
        self.Cygunus = 0
        self.Final = 0
        self.origin = 0
        self.tanjiro = 0
        self.shadow_bit = 0
        self.omen = 0
        self.erda_shower = 0
        self.dominion = 0
        self.janus = 0

def command_with_cooldown(cmd, now, cast_time, cooldown, down_time=0.2, times=3):
    if cast_time == 0 or now - cast_time > cooldown:
        press(cmd, times, down_time=down_time)
        return True
    return False

class Attack(Command):
    """Attacks using in a given direction."""
    def __init__(self, attacks=2):
        super().__init__(locals())
        self.attacks = int(attacks)
        self.shadow_spark = SHADOW_SPARK()
        self.timers = Timers()
        self.shadow_bite = SHADOWBITE()
        self.omen = Omen()
        self.janus = JANUS()
        self.shower = ERDA_SHOWER()

    def main(self):
        now = time.time()
        self.shadow_spark.main()

        for _ in range(self.attacks):
            # if command_with_cooldown(Key.JANUS,now,self.timers.janus,60):
            #     self.timers.janus = now
            #     continue
            if command_with_cooldown(Key.ERDA_SHOWER,now,self.timers.erda_shower,60):
                self.timers.erda_shower = now
                continue
            if command_with_cooldown(Key.DARKOMEN, now, self.timers.omen, 20):
                self.timers.omen = now
                continue
            if command_with_cooldown(Key.SHADOWBITE, now, self.timers.shadow_bit, 15):
                self.timers.shadow_bit = now
                continue
            if command_with_cooldown(Key.DOMINION, now, self.timers.dominion, 180):
                self.timers.dominion = now
                continue
            if command_with_cooldown(Key.ORIGIN, now, self.timers.origin, 360):
                self.timers.origin = now
                continue
            # if command_with_cooldown('9', now, self.timers.tanjiro, 1200):
            #     self.timers.tanjiro = now
            #     continue

        
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.fq
    Should not press any arrow keys, as those are handled by Auto Maple.
    """
    num_presses = 2
    last_pos = config.player_pos
    if direction == 'up':
        num_presses = 2
    if direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 3)
        elif direction == 'up':
             press(Key.JUMP, 2)
    press(Key.JUMP, 2)
    press(Key.SHADOW_SPARK, 1)
    if last_pos == config.player_pos:
        press(Key.JUMP, num_presses)


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
                        key_down('up')
                        time.sleep(0.05)
                        press(Key.JUMP, 2, down_time=0.1)
                        key_up('up')
                    else:
                        key_down('down')
                        time.sleep(0.05)
                        press(Key.JUMP, 1, down_time=0.1)
                        key_up('down')
                        time.sleep(0.05)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Shadowers's buffs once."""

    def __init__(self):
        pass
        super().__init__(locals())
        self.cd120_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        #buffs = [Key.SPEED_INFUSION, Key.HOLY_SYMBOL, Key.SHARP_EYE, Key.COMBAT_ORDERS, Key.ADVANCED_BLESSING]
        now = time.time()

        if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 120:
            press(Key.GREATER_SERVANT,1)
            press(Key.FINAL,1)
            self.cd120_buff_time = now
        if self.cd180_buff_time == 0 or now - self.cd180_buff_time > 180:
            press(Key.SHADOW_ILLUSION,1)
            press(Key.CYGNUS,1)
            self.cd180_buff_time = now
        if self.cd200_buff_time == 0 or now - self.cd200_buff_time > 200:
            press(Key.SHADOW_SPEAR, 1)
            self.cd200_buff_time = now
        if self.cd240_buff_time == 0 or now - self.cd240_buff_time > 240:
            self.cd240_buff_time = now
        if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
            self.cd900_buff_time = now	
class SHADOW_SPARK(Command):

    def main(self):
        press(Key.SHADOW_SPARK, 1)

class ORIGIN(Command):

    def main(self):
        press(Key.ORIGIN, 1)

class SHADOW_ILUSION(Command):

    def main(self):
        press(Key.SHADOW_ILLUSION, 1)

class FINAL(Command):

    def main(self):
        press(Key.FINAL, 1)
class CYGNUS(Command):

    def main(self):
        press(Key.CYGNUS, 1)

class GREATER_SERVANT(Command):

    def main(self):
        press(Key.GREATER_SERVANT, 1)

class ERDA_SHOWER(Command):

    def main(self):
        press(Key.ERDA_SHOWER, 1)

class SHADOW_SPEAR(Command):

    def main(self):
        press(Key.SHADOW_SPEAR, 1)

class SHADOWBITE(Command):

    def main(self):
        press(Key.SHADOWBITE, 1)
class JANUS(Command):

    def main(self):
        press(Key.JANUS, 1)
class Omen(Command):

    def main(self):
        press(Key.DARKOMEN, 1)

class FlashJump(Command):
    """Performs a flash jump in the given direction."""

    def __init__(self):
        super().__init__(locals())

    def main(self):
        press(Key.FLASH_JUMP, 2)

class RopeLift(Command):
    """Performs a flash jump in the given direction."""

    def __init__(self):
        super().__init__(locals())

    def main(self):
        press(Key.ROPE_LIFT, 1)

class SHADOW_LEAP(Command):
    """Uses 'Showdown' once."""

    def main(self):
        press(Key.SHADOW_LEAP, 1)

class DOMINION(Command):
    """Uses 'Showdown' once."""

    def main(self):
        press(Key.DOMINION, 1)
        press('e',1)

class Def(Command):
    """Uses each of Bishop's buffs once. Uses 'Haku Reborn' whenever it is available."""

    def __init__(self):
        super().__init__(locals())

    def main(self):
        return
    
# class Adjust(Command):
#     """Fine-tunes player position using small movements."""

#     def __init__(self, x, y, max_steps=5):
#         super().__init__(locals())
#         self.target = (float(x), float(y))
#         self.max_steps = settings.validate_nonnegative_int(max_steps)

#     def main(self):
#         counter = self.max_steps
#         toggle = True
#         error = utils.distance(config.player_pos, self.target)
#         while config.enabled and counter > 0 and error > settings.adjust_tolerance:
#             if toggle:
#                 d_x = self.target[0] - config.player_pos[0]
#                 threshold = settings.adjust_tolerance / math.sqrt(2)
#                 if abs(d_x) > threshold:
#                     walk_counter = 0
#                     if d_x < 0:
#                         key_down('left')
#                         while config.enabled and d_x < -1 * threshold and walk_counter < 60:
#                             time.sleep(0.05)
#                             walk_counter += 1
#                             d_x = self.target[0] - config.player_pos[0]
#                         key_up('left')
#                     else:
#                         key_down('right')
#                         while config.enabled and d_x > threshold and walk_counter < 60:
#                             time.sleep(0.05)
#                             walk_counter += 1
#                             d_x = self.target[0] - config.player_pos[0]
#                         key_up('right')
#                     counter -= 1
#             else:
#                 d_y = self.target[1] - config.player_pos[1]
#                 if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
#                     if d_y < 0:
#                         press(Key.JUMP, 1)
#                     else:
#                         key_down('down')
#                         time.sleep(0.05)
#                         press(Key.JUMP, 3, down_time=0.1)
#                         key_up('down')
#                         time.sleep(0.05)
#                     counter -= 1
#             error = utils.distance(config.player_pos, self.target)
#             toggle = not toggle