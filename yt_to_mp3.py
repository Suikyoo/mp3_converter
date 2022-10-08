import pytube, os, subprocess

def mp3_converter(link, file_name):
    path = os.path.abspath('.')

    print('processing')
    audio = pytube.YouTube(link).streams.filter(only_audio=True).first()
      
    # download the file
    print('downloading')
    out_file = audio.download(output_path='.')
    
    # save the file
    base, ext = os.path.splitext(out_file)
    default_name = "video" + file_name 
    os.rename(base + ext, default_name + ext)
    
    #converts mp4 container to real mp3
    subprocess.run(['ffmpeg', '-i',
                    os.path.join(path, default_name + '.mp4'),
                    os.path.join(path, file_name + '.mp3')
                    ])
    
    print("download successful")


links = ['https://www.youtube.com/watch?v=GZqi2Nv2M04']
        
for index, i in enumerate(links):
    mp3_converter(i, "audio_" + str(index))
