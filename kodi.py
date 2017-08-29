"""
A helper library of functions for interacting with the Kodi JSON-RPC API.
"""
from __future__ import absolute_import, print_function, division
from fuzzywuzzy import fuzz

def find_films_matching(kodi, search):
    """
    Search the movie database for all the films matching a string.

    Parameters
    ----------

    Kodi : `beekeeper.api.API`
        The current Kodi connection.

    search : `search`
        The search string

    Returns
    -------

    results: `list`
        All the results matching the search.
        (list of 'label', 'movieid' dicts.)
    """
    movies = kodi.VideoLibrary.GetMovies()['result']['movies']
    results = []
    for m in movies:
        if search in m['label'].lower():
            results.append(m)
    return results

def play_youtube_video(kodi,search):
    dirname="plugin://plugin.video.youtube/kodion/search/query/?q="+search
    resp=kodi.Files.GetDirectory(directory=dirname)
    videoid=resp['result']['files'][3]['file']
    play_file(kodi,videoid)
    
def play_youtube_playlist(kodi,search):
    dirname="plugin://plugin.video.youtube/kodion/search/query/?q="\
            +search+"&search_type=playlist"
    resp=kodi.Files.GetDirectory(directory=dirname)
    playid=resp['result']['files'][3]['file']
    play_playlist(kodi,playid)
    
def play_radio(kodi,radio_name):
    sources=kodi.Files.GetSources("music")
    radio_path=None
    for i in sources['result']['sources']:
        if i['label']=='Radio':
            radio_path=i['file']
        break
    if not radio_path is None:
        radio_list=kodi.Files.GetDirectory(radio_path)
        best_score = 0
        best_entity = None
        for radio in radio_list['result']['files']:
            try:
                    score = fuzz.ratio(radio_name, radio['label'].lower())
                    if score > best_score:
                        best_score = score
                        best_radio = radio['file']
            except KeyError:
                pass
        play_file(kodi,best_radio) 

def play_file(kodi, file):
    """
    Play a movie by id.
    """
#    LOGGER.debug("playing: $s" % file)
    kodi.Playlist.Clear(playlistid=1)
    kodi.Playlist.Add(playlistid=1, item={'file': file})
    kodi.Player.Open(item={'playlistid': 1})
    
def play_playlist(kodi,playlist):
    kodi.Playlist.Clear(playlistid=1)
    kodi.Playlist.Add(playlistid=1, item={'directory': playlist})
    kodi.Player.SetShuffle(playerid=1,shuffle=True)
    kodi.Player.Open(item={'playlistid': 1})
                     
def play_film(kodi, movieid):
    """
    Play a movie by id.
    """
    kodi.Playlist.Clear(playlistid=1)
    kodi.Playlist.Add(playlistid=1, item={'movieid': movieid})
    kodi.Player.Open(item={'playlistid': 1})


def stop_playback(kodi):
    players = kodi.Player.GetActivePlayers()['result']
    for player in players:
        kodi.Player.Stop(playerid=player['playerid'])


def playpause_playback(kodi):
    players = kodi.Player.GetActivePlayers()['result']
    for player in players:
        kodi.Player.PlayPause(playerid=player['playerid'])
