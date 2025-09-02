import time
import threading

import lib.logger
from settings import *


class Clock:
    def __init__(self):
        self.start_time = None
        self._stop_flag = False
        self._thread = None

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
            self.check_rune_spawn(total_seconds)
            time.sleep(0.5)

    def check_forrest_creep_spawn(self, total_seconds, m):
        if total_seconds % FORREST_CREEPS_SPAWN_FREQUENCY_IN_SECONDS == 0 and m != 0:
            lib.logger.info("Forrest creeps spawned", 4)
            self.beep()

    def check_rune_spawn(self, total_seconds):
        if total_seconds % RUNE_SPAWN_FREQUENCY_IN_SECONDS == 0:
            lib.logger.info("Runes spawned", 4)
            self.beep()

    def check_lane_creep_spawn(self, total_seconds):
        if total_seconds % LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS == 0:
            lib.logger.info("Lane creeps spawned", 4)
            self.beep()
            time.sleep(1)  # prevent double-beep in the same second

    def beep(self):
        h, m, s, total = self.get_time_in_hours_minutes_seconds_and_total_seconds_passed()
        lib.logger.info(f"Internal timer is {h:02}:{m:02}:{s:02}",4)
        lib.logger.info("BEEP", 4)
