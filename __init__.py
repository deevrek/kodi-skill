from __future__ import absolute_import, print_function

from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill,intent_handler
from mycroft.util.log import getLogger

from kodipydent import Kodi
import sys
sys.path.append(dirname(__file__))
import kodi
#__import__('kodi')

_author__ = 'Stuart Mumford'

LOGGER = getLogger(__name__)


class KodiSkill(MycroftSkill):
    """
    A Skill to control playback on a Kodi instance via the json-rpc interface.
    """

    def __init__(self):
        super(KodiSkill, self).__init__(name="KodiSkill")
        try:
            self.kodi = Kodi(self.config.get('host'),self.config.get('user','kodi'),
                         self.config.get('password',''))
        except:
            LOGGER.error("Unable to inizialize Kodi:",exc_info=True)
#     def initialize(self):
#         self.load_data_files(dirname(__file__))

#         self.register_regex("film (?P<Film>.*)")
#         self.register_regex("movie (?P<Film>.*)")
#         self.register_regex("with (?P<Film>.*)")
#         self.register_regex("containing (?P<Film>.*)")
#         self.register_regex("matching (?P<Film>.*)")
#         self.register_regex("including (?P<Film>.*)")

#        self.build_play_film_intent()
#        self.build_film_search_intent()
   
    @intent_handler(IntentBuilder('PlayIntent')
                    .require("PlayKeyword").require("MediaKeyword")
                    .require("YoutubeSearch")
                    .optionally("PlaylistKeyword"))
    def play_youtube_kodi(self,message):
        query=message.data.get('YoutubeSearch').replace(" ","+")
        is_a_playlist=False
        if "PlaylistKeyword" in message.data:
            kodi.play_youtube_playlist(self.kodi,query)
        else:
            kodi.play_youtube_video(self.kodi,query)
            
    @intent_handler(IntentBuilder('PlayRadioIntent')
                    .require("PlayKeyword").require("MediaKeyword")
                    .require("RadioSearch"))
    def play_radio_kodi(self,message):
        query="radio "+message.data.get('RadioSearch')
        kodi.play_radio(self.kodi,query)
        
    def play_youtube_kodi(self,message):
        if message.data['MediaKeyword']=="youtube":
            query=message.data.get('YoutubeSearch').replace(" ","+")
            kodi.play_youtube_search(self.kodi,query)              
    
    def play_youtube_intent(search):
        query=search.replace(" ","+")
        try:
            kodi.play_search_youtube(query)
        except:
            LOGGER.error("search on kodi failed")
            

    def stop(self):
        kodi.stop_playback(self.kodi)


def create_skill():
    return KodiSkill()
