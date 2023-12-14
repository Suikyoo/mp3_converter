import pytube, os, subprocess

def mp3_converter(link, path=None):
    if not path:
        path = os.path.abspath('.')

    print('processing')
    audio = pytube.YouTube(link).streams.filter(only_audio=True).first()
      
    # download the file
    print('downloading')
    out_file = audio.download(output_path=path)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    
    #converts mp4 container to real mp3
    subprocess.run(['ffmpeg', '-i',
                    os.path.join(path, base + ext),
                    os.path.join(path, base + '.mp3')
                    ])
    
    print("download successful")
