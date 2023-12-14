from yt_to_mp3 import *

links = ['https://www.youtube.com/watch?v=GZqi2Nv2M04']
        
os.mkdir("ppg")
for index, i in enumerate(links):
    mp3_converter(i, "ppg")
