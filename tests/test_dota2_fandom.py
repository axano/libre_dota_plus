import unittest

import lib.logger
import lib.data_retrieval.dota2_fandom
import lib.file_manipulation


class TestDota2Fandom(unittest.TestCase):
    def test_list_heroes_bad_against_not_empty(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        heroes_list = lib.data_retrieval.dota2_fandom.get_heroes_bad_against("Abaddon")
        self.assertNotEqual(len(heroes_list), 0)

    def test_list_heroes_bad_against_contains_specific_hero(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        heroes_list = lib.data_retrieval.dota2_fandom.get_heroes_bad_against("Abaddon")
        self.assertIn("Axe", heroes_list)

    def test_list_heroes_good_against_not_empty(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        heroes_list = lib.data_retrieval.dota2_fandom.get_heroes_good_against("Abaddon")
        self.assertNotEqual(len(heroes_list), 0)

    def test_list_heroes_good_against_contains_specific_hero(self):
        lib.logger.info("Running " + self._testMethodName + "()", 0)
        heroes_list = lib.data_retrieval.dota2_fandom.get_heroes_good_against("Abaddon")
        self.assertIn("Mirana", heroes_list)

