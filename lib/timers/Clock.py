import time
import threading
from playsound3 import playsound
import lib.logger
from settings import *


class SpawnEvent:
    def __init__(self, name, frequency, sound_path, require_nonzero_minute=True):
        self.name = name
        self.frequency = frequency
        self.sound_path = sound_path
        self.require_nonzero_minute = require_nonzero_minute
        self.last_triggered = None

    def should_trigger(self, total_seconds, minutes):
        """Check if the event should trigger at this time."""
        if total_seconds % self.frequency != 0:
            return False
        if self.require_nonzero_minute and minutes == 0:
            return False
        if self.last_triggered == total_seconds:
            return False
        return True

    def trigger(self, total_seconds):
        """Mark as triggered and log the event."""
        self.last_triggered = total_seconds
        lib.logger.info(f"{self.name} spawned", 4)
        threading.Thread(target=playsound, args=(self.sound_path,), daemon=True).start()


class Clock:
    def __init__(self):
        self.start_time = None
        self._stop_flag = False
        self._thread = None

        # Configure all events here in one place
        self.events = [
            SpawnEvent("Lane creeps", LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/lane_creeps_spawning.mp3", False),
            SpawnEvent("Forrest creeps", FORREST_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/forrest_creeps_spawning.mp3"),
            SpawnEvent("Runes", RUNE_SPAWN_FREQUENCY_IN_SECONDS, "sounds/runes_spawning.mp3"),
            SpawnEvent("Bounty runes", BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS, "sounds/bounty_runes_spawning.mp3", False),
            SpawnEvent("Wisdom runes", WISDOM_RUNE_FREQUENCY_IN_SECONDS, "sounds/wisdom_runes_spawning.mp3"),
            SpawnEvent("Lotus", LOTUS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/lotus_spawning.mp3"),
            SpawnEvent("Tormentor", TORMENTOR_SPAWN_FREQUENCY_IN_SECONDS, "sounds/tormentor_spawning.mp3"),
        ]

    def start(self):
        self.start_time = time.time()
        self._stop_flag = False
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()

    def elapsed(self):
        if self.start_time is None:
            raise ValueError("Timer has not been started yet.")
        return round(time.time() - self.start_time)

    def get_time(self):
        total_seconds = self.elapsed()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds, total_seconds

    def _check_loop(self):
        while not self._stop_flag:
            h, m, s, total_seconds = self.get_time()
            for event in self.events:
                if event.should_trigger(total_seconds, m):
                    event.trigger(total_seconds)
            time.sleep(0.4)

    def stop(self):
        self._stop_flag = True
