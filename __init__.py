#!/usr/bin/env python3
import re
import json
import inflect
from mycroft import MycroftSkill, intent_file_handler

from pyradios import RadioBrowser
from word2number import w2n

from mycroft.skills.common_play_skill import CommonPlaySkill, CPSMatchLevel
from mycroft.util.log import LOG

stations = {
    "1": "http://icecast4.play.cz/krokodyl128.mp3.m3u",
    "2": "https://listen.happychristmasradio.net/"
}

def find_preset (phrase):
    numbers_regex = r"\b(one|two|three|four|five|six|seven|eight|nine)\b"
    num = re.findall(numbers_regex, phrase)
    for number in num:
        phrase = phrase.replace(number, str(w2n.word_to_num(number)))
    n = re.search("\d+", phrase).group()
    return phrase, CPSMatchLevel.EXACT, {"url": stations [n]}
        

class InetRadio(CommonPlaySkill):
    def __init__(self):
        super().__init__(name="InetRadio")

    def CPS_match_query_phrase(self, phrase):
        search_phrase = phrase.lower()
        return find_preset (phrase)

    def CPS_start(self, phrase, data):
        if self.audioservice.is_playing:
            self.audioservice.stop()
        url = data["url"]
        LOG.info(f"Playing from {url}")
        self.audioservice.play(url)
      
    @intent_file_handler('radio.inet.intent')
    def handle_radio_inet(self, message):
        self.speak_dialog('radio.inet')
        matched_station = find_preset(message.data["preset"])
        LOG.info(f"Playing from {matched_station[2]['url']}")
        self.CPS_play(matched_station[2]["url"])


def create_skill():
    return InetRadio()

