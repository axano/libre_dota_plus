import time
import threading
from gtts import gTTS
import lib.logger
from settings import *
from playsound3 import playsound

class Clock:
    def __init__(self):
        self.start_time = None
        self._stop_flag = False
        self._thread = None
        self.last_time_line_creeps_spawned = None
        self.last_time_rune_spawned = None
        self.last_time_bounty_rune_spawned = None
        self.last_time_wisdom_rune_spawned = None
        self.last_time_lotus_spawned = None
        self.last_time_tormentor_spawned = None
        self.last_time_forrest_creeps_spawned = None
        self.sound_file_path = "sounds/alert.mp3"
        self.bounty_rune_spawning_sound_path = "sounds/bounty_runes_spawning.mp3"
        self.runes_spawning_sound_path = "sounds/runes_spawning.mp3"
        self.wisdom_rune_spawning_sound_path = "sounds/wisdom_runes_spawning.mp3"
        self.forrest_creeps_spawning_sound_path = "sounds/forrest_creeps_spawning.mp3"
        self.lane_creeps_spawning_sound_path = "sounds/lane_creeps_spawning.mp3"
        self.lotus_spawning_sound_path = "sounds/lotus_spawning.mp3"
        self.tormentor_spawning_sound_path = "sounds/tormentor_spawning.mp3"

    def start(self):
        self.start_time = time.time()
        self._stop_flag = False
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()

    def elapsed(self):
        if self.start_time is None:
            raise ValueError("Timer has not been started yet.")
        return round(time.time() - self.start_time)

    def get_time_in_hours_minutes_seconds_and_total_seconds_passed(self):
        total_seconds = round(self.elapsed())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds, total_seconds

    def _check_loop(self):
        while not self._stop_flag:
            h, m, s, total_seconds = self.get_time_in_hours_minutes_seconds_and_total_seconds_passed()
            self.check_lane_creep_spawn(total_seconds)
            self.check_forrest_creep_spawn(total_seconds, m)
            self.check_rune_spawn(total_seconds, m)
            self.check_bounty_rune_spawn(total_seconds)
            self.check_tormentor_spawn(total_seconds, m)
            self.check_lotus_spawn(total_seconds, m)
            self.check_wisdom_rune_spawn(total_seconds, m)
            time.sleep(0.4)

    def check_forrest_creep_spawn(self, total_seconds, m):
        if total_seconds % FORREST_CREEPS_SPAWN_FREQUENCY_IN_SECONDS == 0 and m != 0 and self.last_time_forrest_creeps_spawned != total_seconds:
            self.last_time_forrest_creeps_spawned = total_seconds
            lib.logger.info("Forrest creeps spawned", 4)
            self.play_sound(self.forrest_creeps_spawning_sound_path)
            return True
        return False

    def check_rune_spawn(self, total_seconds, m):
        if total_seconds % RUNE_SPAWN_FREQUENCY_IN_SECONDS == 0 and m != 0 and self.last_time_rune_spawned != total_seconds:
            self.last_time_rune_spawned = total_seconds
            lib.logger.info("Runes spawned", 4)
            self.play_sound(self.runes_spawning_sound_path)
            return True
        return False

    def check_wisdom_rune_spawn(self, total_seconds, m):
        if total_seconds % WISDOM_RUNE_FREQUENCY_IN_SECONDS == 0 and m != 0 and self.last_time_wisdom_rune_spawned != total_seconds:
            self.last_time_wisdom_rune_spawned = total_seconds
            lib.logger.info("Wisdom runes spawned", 4)
            self.play_sound(self.wisdom_rune_spawning_sound_path)
            return True
        return False

    def check_lotus_spawn(self, total_seconds, m):
        if total_seconds % LOTUS_SPAWN_FREQUENCY_IN_SECONDS == 0 and m != 0 and self.last_time_lotus_spawned != total_seconds:
            self.last_time_lotus_spawned = total_seconds
            lib.logger.info("Lotuses spawned", 4)
            self.play_sound(self.lotus_spawning_sound_path)
            return True
        return False

    def check_tormentor_spawn(self, total_seconds, m):
        if total_seconds % TORMENTOR_SPAWN_FREQUENCY_IN_SECONDS == 0 and m != 0 and self.last_time_tormentor_spawned != total_seconds:
            self.last_time_tormentor_spawned = total_seconds
            lib.logger.info("Tormentors spawned", 4)
            self.play_sound(self.tormentor_spawning_sound_path)
            return True
        return False

    def check_bounty_rune_spawn(self, total_seconds):
        if total_seconds % BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS == 0 and self.last_time_bounty_rune_spawned != total_seconds:
            self.last_time_bounty_rune_spawned = total_seconds
            lib.logger.info("Bounty runes spawned", 4)
            self.play_sound(self.bounty_rune_spawning_sound_path)
            return True
        return False

    def check_lane_creep_spawn(self, total_seconds):
        if total_seconds % LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS == 0 and self.last_time_line_creeps_spawned != total_seconds:
            self.last_time_line_creeps_spawned = total_seconds
            lib.logger.info("Lane creeps spawned", 4)
            self.play_sound(self.lane_creeps_spawning_sound_path)
            return True
        return False

    def play_sound(self, sound):
        h, m, s, total = self.get_time_in_hours_minutes_seconds_and_total_seconds_passed()
        # lib.logger.info(f"Internal timer is {h: 02}: {m: 02}: {s: 02}", 4)
        threading.Thread(target=playsound, args=(sound,), daemon=True).start()


