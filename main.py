import lib.timers.Clock
import time

from gtts import gTTS

def main ():
    clock = lib.timers.Clock.Clock()
    input("Press enter to start timer")
    clock.start()
    while True:
        time.sleep(1)


def debug():
    clock = lib.timers.Clock.Clock()
    # chat_to_speech("Wisdom runes spawning.")

def chat_to_speech(text):
    # Convert text to speech
    tts = gTTS(text=text, lang="en" , tld="us")
    filename = "sounds/response.mp3"
    tts.save(filename)


# debug()
main()