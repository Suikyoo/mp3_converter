from yt_to_mp3 import *
#playlist must not be private
play_list = pytube.contrib.playlist.Playlist("https://www.youtube.com/playlist?list=PLPPtg2ESewWhydSXHV9CP-BV7sEXzbfaR")

try: 
    os.mkdir(play_list.title)
except FileExistsError: 
    pass

for link in play_list.video_urls:
    mp3_converter(link, path=play_list.title)
