import requests
import lib.logger
from bs4 import BeautifulSoup
import lib.data_retrieval.dota2_fandom
import lib.timers.Clock
import time

time_to_sleep = 180

clock = lib.timers.Clock.Clock()
clock.start()
time.sleep(time_to_sleep)
