import unittest
import time
import lib.logger
import lib.timers.Clock


class TestClock(unittest.TestCase):
    def test_Clock_ticks_when_started(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        time_to_sleep = 2
        clock = lib.timers.Clock.Clock()
        clock.start()
        time.sleep(time_to_sleep)
        elapsed_time = clock.elapsed()
        self.assertEqual(elapsed_time, time_to_sleep)

    def test_check_forrest_creeps_spawned(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        clock = lib.timers.Clock.Clock()
        clock.start()
        self.assertFalse(clock.check_forrest_creep_spawn(59, 1))
        self.assertFalse(clock.check_forrest_creep_spawn(61, 1))
        self.assertFalse(clock.check_forrest_creep_spawn(59, 0))
        self.assertTrue(clock.check_forrest_creep_spawn(60, 1))
        self.assertFalse(clock.check_forrest_creep_spawn(60, 0))
        self.assertFalse(clock.check_forrest_creep_spawn(160, 0))
        self.assertTrue(clock.check_forrest_creep_spawn(120, 2))

    def test_check_rune_spawn(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        clock = lib.timers.Clock.Clock()
        clock.start()
        self.assertFalse(clock.check_rune_spawn(59, 1))
        self.assertFalse(clock.check_rune_spawn(121, 0))
        self.assertFalse(clock.check_rune_spawn(121, 1))
        self.assertFalse(clock.check_rune_spawn(119, 0))
        self.assertFalse(clock.check_rune_spawn(119, 1))
        self.assertTrue(clock.check_rune_spawn(120, 2))
        self.assertTrue(clock.check_rune_spawn(240, 4))
        self.assertFalse(clock.check_rune_spawn(60, 0))
        self.assertFalse(clock.check_rune_spawn(120, 0))
        self.assertFalse(clock.check_rune_spawn(160, 0))

    def test_check_wisdom_rune_spawn(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        clock = lib.timers.Clock.Clock()
        clock.start()
        self.assertFalse(clock.check_wisdom_rune_spawn(421, 7))
        self.assertFalse(clock.check_wisdom_rune_spawn(421, 0))
        self.assertFalse(clock.check_wisdom_rune_spawn(419, 6))
        self.assertFalse(clock.check_wisdom_rune_spawn(420, 0))
        self.assertFalse(clock.check_wisdom_rune_spawn(422, 1))
        self.assertTrue(clock.check_wisdom_rune_spawn(840, 14))
        self.assertTrue(clock.check_wisdom_rune_spawn(1260, 21))
        self.assertFalse(clock.check_wisdom_rune_spawn(630, 10))
        self.assertFalse(clock.check_wisdom_rune_spawn(120, 0))
        self.assertFalse(clock.check_wisdom_rune_spawn(160, 0))

    def test_check_lotus_spawn(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        clock = lib.timers.Clock.Clock()
        clock.start()
        self.assertFalse(clock.check_lotus_spawn(181, 3))
        self.assertFalse(clock.check_lotus_spawn(181, 0))
        self.assertFalse(clock.check_lotus_spawn(179, 2))
        self.assertFalse(clock.check_lotus_spawn(180, 0))
        self.assertFalse(clock.check_lotus_spawn(181, 3))
        self.assertTrue(clock.check_lotus_spawn(180, 3))
        self.assertFalse(clock.check_lotus_spawn(160, 6))
        self.assertTrue(clock.check_lotus_spawn(1800, 30))
        self.assertFalse(clock.check_lotus_spawn(630, 10))
        self.assertFalse(clock.check_lotus_spawn(120, 0))
        self.assertFalse(clock.check_lotus_spawn(160, 0))

    def test_check_tormentor_spawn(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        clock = lib.timers.Clock.Clock()
        clock.start()
        self.assertFalse(clock.check_tormentor_spawn(599, 9))
        self.assertFalse(clock.check_tormentor_spawn(600, 0))
        self.assertFalse(clock.check_tormentor_spawn(601, 10))
        self.assertFalse(clock.check_tormentor_spawn(605, 5))
        self.assertFalse(clock.check_tormentor_spawn(601, 11))
        self.assertTrue(clock.check_tormentor_spawn(600, 10))
        self.assertTrue(clock.check_tormentor_spawn(1200, 20))
        self.assertFalse(clock.check_tormentor_spawn(630, 10))
        self.assertFalse(clock.check_tormentor_spawn(9999, 10))
        self.assertFalse(clock.check_tormentor_spawn(160, 0))