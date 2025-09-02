import unittest

import lib.logger
import lib.file_manipulation
import settings


class TestLogger(unittest.TestCase):
    def test_write_log_to_file(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        test_message = "test123 message123"
        lib.logger.write_log_to_file(test_message)
        last_line = lib.file_manipulation.retrieve_last_line(settings.LOG_PATH)
        self.assertEqual(test_message, last_line)
        lib.file_manipulation.delete_last_line_of_file(settings.LOG_PATH)



