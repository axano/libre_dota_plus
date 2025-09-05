import unittest
import time
import lib.logger
from lib.timers.Clock import Clock, SpawnEvent
from settings import (
    FORREST_CREEPS_SPAWN_FREQUENCY_IN_SECONDS,
    RUNE_SPAWN_FREQUENCY_IN_SECONDS,
    WISDOM_RUNE_FREQUENCY_IN_SECONDS,
    LOTUS_SPAWN_FREQUENCY_IN_SECONDS,
    TORMENTOR_SPAWN_FREQUENCY_IN_SECONDS,
    LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS,
    BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS,
)


class TestClock(unittest.TestCase):
    def test_clock_ticks_when_started(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        clock = Clock()
        clock.start()
        time.sleep(2)
        elapsed_time = clock.elapsed()
        self.assertIn(elapsed_time, [1, 2])  # allow slight timing variation

    def test_forrest_creep_event(self):
        event = SpawnEvent("Forrest creeps", FORREST_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/forrest_creeps_spawning.mp3")
        self.assertFalse(event.should_trigger(59, 1))
        self.assertFalse(event.should_trigger(60, 0))  # minute = 0 not allowed
        self.assertTrue(event.should_trigger(60, 1))
        event.trigger(60)
        self.assertFalse(event.should_trigger(60, 1))  # duplicate prevention

    def test_rune_event(self):
        event = SpawnEvent("Runes", RUNE_SPAWN_FREQUENCY_IN_SECONDS, "sounds/runes_spawning.mp3")
        self.assertFalse(event.should_trigger(119, 1))
        self.assertTrue(event.should_trigger(120, 2))
        event.trigger(120)
        self.assertFalse(event.should_trigger(120, 2))

    def test_wisdom_rune_event(self):
        event = SpawnEvent("Wisdom runes", WISDOM_RUNE_FREQUENCY_IN_SECONDS, "sounds/wisdom_runes_spawning.mp3")
        self.assertFalse(event.should_trigger(419, 6))
        self.assertTrue(event.should_trigger(420, 7))
        event.trigger(420)
        self.assertFalse(event.should_trigger(420, 7))

    def test_lotus_event(self):
        event = SpawnEvent("Lotus", LOTUS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/lotus_spawning.mp3")
        self.assertFalse(event.should_trigger(179, 2))
        self.assertTrue(event.should_trigger(180, 3))

    def test_tormentor_event(self):
        event = SpawnEvent("Tormentor", TORMENTOR_SPAWN_FREQUENCY_IN_SECONDS, "sounds/tormentor_spawning.mp3")
        self.assertFalse(event.should_trigger(599, 9))
        self.assertTrue(event.should_trigger(600, 10))
        event.trigger(600)
        self.assertFalse(event.should_trigger(600, 10))

    def test_lane_creep_event(self):
        event = SpawnEvent("Lane creeps", LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/lane_creeps_spawning.mp3", require_nonzero_minute=False)
        self.assertTrue(event.should_trigger(LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, 0))
        event.trigger(LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS)
        self.assertFalse(event.should_trigger(LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, 0))

    def test_bounty_rune_event(self):
        event = SpawnEvent("Bounty runes", BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS, "sounds/bounty_runes_spawning.mp3", require_nonzero_minute=False)
        self.assertTrue(event.should_trigger(BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS, 0))
        event.trigger(BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS)
        self.assertFalse(event.should_trigger(BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS, 0))

    def test_clock_has_expected_events(self):
        clock = Clock()
        event_map = {e.name: e.sound_path for e in clock.events}
        expected = {
            "Lane creeps": "sounds/lane_creeps_spawning.mp3",
            "Forrest creeps": "sounds/forrest_creeps_spawning.mp3",
            "Runes": "sounds/runes_spawning.mp3",
            "Bounty runes": "sounds/bounty_runes_spawning.mp3",
            "Wisdom runes": "sounds/wisdom_runes_spawning.mp3",
            "Lotus": "sounds/lotus_spawning.mp3",
            "Tormentor": "sounds/tormentor_spawning.mp3",
        }
        self.assertEqual(event_map, expected)


if __name__ == "__main__":
    unittest.main()
