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

