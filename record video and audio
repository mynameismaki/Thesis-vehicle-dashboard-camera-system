import os
import shutil
import psutil
import glob
import time
import subprocess
from datetime import datetime
check_interval = 1
cmd = "sudo systemctl stop raspivid"
time.sleep(10)
while True:
    try:
        if not os.path.exists('/home/pi/Sync/'):
            os.makedirs('/home/pi/Sync/')
        
        if not os.path.exists('/home/pi/Videos/'):
            os.makedirs('/home/pi/Videos/')
            
        # Disclaimer
        if not os.path.exists('/home/pi/Sync/README.txt'):
            with open("/home/pi/Sync/README.txt", "w") as f:
                f.write("This folder is intended for video footages captured by the raspberry pi, do not put any files under this folder.")
                
        # Check if usb microphone is available:
        is_audio = subprocess.run(['arecord', '-l'], capture_output = True)
        audio_exist = is_audio.stdout.decode()
        
        # Directory of files
        files = os.listdir('/home/pi/Videos/')
        
        # Initial Setup for Directory
        if files:
            if os.path.exists('/home/pi/Videos/video.h264') and os.path.exists('/home/pi/Videos/timestamp.pts') and os.path.exists('/home/pi/Videos/audio.wav'):
                # Check if datetime text file exists
                if os.path.exists('/home/pi/Videos/datetime.txt'):
                    with open('/home/pi/Videos/datetime.txt', 'r') as f:
                        timestamp = f.read()
                
                else:
                    # Get the current timestamp
                    timestamp = datetime.now().strftime('%a%b%-d_%I-%M-%S-%p_%Y')
                    
                os.rename('/home/pi/Videos/video.h264', '/home/pi/Merger/{}.h264'.format(timestamp))
                os.rename('/home/pi/Videos/audio.wav', '/home/pi/Merger/{}.wav'.format(timestamp))
                os.rename('/home/pi/Videos/timestamp.pts', '/home/pi/Merger/{}.pts'.format(timestamp))
            elif os.path.exists('/home/pi/Videos/video.h264') and os.path.exists('/home/pi/Videos/timestamp.pts'):
                # Check if datetime exists
                if os.path.exists('/home/pi/Videos/datetime.txt'):
                    with open('/home/pi/Videos/datetime.txt', 'r') as f:
                        timestamp = f.read()
                
                else:
                    # Get the current timestamp
                    timestamp = datetime.now().strftime('%a%b%-d_%I-%M-%S-%p_%Y')
                
                # Check if movie.mkv exists
                if os.path.exists('/home/pi/Videos/movie.mkv'):
                    os.remove('/home/pi/Videos/movie.mkv')
                    
                # Merge video only
                mergevideo = ['bash', '/home/pi/mergevid.sh']
                mergevideo_run = subprocess.Popen(mergevideo)
                mergevideo_run.wait()
                mergevideo_run.terminate()
                
                # Rename the temporary output to its timestamp
                output_file = '/home/pi/Sync/' + timestamp + '.mkv'
                os.rename('/home/pi/Videos/movie.mkv', output_file)
                
                # Remove video file
                os.remove('/home/pi/Videos/video.h264')
                os.remove('/home/pi/Videos/timestamp.pts')
                
                time.sleep(5)
            
            else:
                # Delete all files in the video directory
                for file in files:
                    file_path = os.path.join('/home/pi/Videos/', file)
                    os.remove(file_path)
                    
        # Get the current disk usage
        path = '/'
        disk = psutil.disk_usage(path)
        
        # Check if the disk usage is greater than 85%
        while disk.percent >= 79:
            mkv_files = glob.glob('/home/pi/Sync/*.mkv')
            if len(mkv_files) == 0:
                # No mkv files found, exit the program
                raise Exception("No .mkv files found, exiting the program...")
                
            # Delete the oldest mkv file in the sync directory
            oldest_file = sorted(glob.glob(os.path.join('/home/pi/Sync/', '*.mkv')), key=os.path.getctime)[0]
            os.remove(oldest_file)
            disk = psutil.disk_usage(path)

        # If microphone is connected
        if 'USB Audio' in audio_exist:
            # Get the current timestamp
            timestamp = datetime.now().strftime('%a%b%-d_%I-%M-%S-%p_%Y')

            # Store in a text file to remember datetime
            with open('/home/pi/Videos/datetime.txt', 'w') as f:
                f.write(timestamp)

            # Record Video and Audio Simultaneously
            video = ['bash', '/home/pi/recordvideo.sh']
            audio = ['bash', '/home/pi/recordaudio.sh']
            
            video_run = subprocess.Popen(video)
            audio_run = subprocess.Popen(audio)
            for i in range(int(300/check_interval)):
                time.sleep(check_interval)
                is_audio = subprocess.run(['arecord', '-l'], capture_output = True)
                audio_exist = is_audio.stdout.decode()
                if 'USB Audio' not in audio_exist:
                    print("USB microphone not detected, proceeding to record video only.")
                    
                    audio_run.terminate()
                    
                    # Concatenate '_video-only'
                    timestamp += '_video-only'
                    
                    # Update datetime.txt
                    with open('/home/pi/Videos/datetime.txt', 'w') as f:
                        f.write(timestamp)
                    
                    # Remove Audio Wav
                    os.remove('/home/pi/Videos/audio.wav')
                    
                    video_run.wait()
                    
                    # Merge video only
                    mergevideo = ['bash', '/home/pi/mergevid.sh']
                    mergevideo_run = subprocess.Popen(mergevideo)
                    mergevideo_run.wait()
                    mergevideo_run.terminate()
                    
                    # Check if datetime text file exists
                    if os.path.exists('/home/pi/Videos/datetime.txt'):
                        with open('/home/pi/Videos/datetime.txt', 'r') as f:
                            timestamp = f.read()
                    
                    # Rename the temporary output to its timestamp
                    output_file = '/home/pi/Sync/' + timestamp + '.mkv'
                    os.rename('/home/pi/Videos/movie.mkv', output_file)
                    
                    # Remove video file
                    os.remove('/home/pi/Videos/video.h264')
                    os.remove('/home/pi/Videos/timestamp.pts')
                    
                    time.sleep(6)
                    
                    # Skip loop
                    raise ValueError('USB microphone unplugged, video still recorded.')
                
            video_run.wait()
            audio_run.wait()
            video_run.terminate()
            audio_run.terminate()
            
            os.rename('/home/pi/Videos/video.h264', '/home/pi/Merger/{}.h264'.format(timestamp))
            os.rename('/home/pi/Videos/audio.wav', '/home/pi/Merger/{}.wav'.format(timestamp))
            os.rename('/home/pi/Videos/timestamp.pts', '/home/pi/Merger/{}.pts'.format(timestamp))
            
            # Grace Period
            time.sleep(6)
            
            raise ValueError('Video with audio recorded')    
            
        else:
            print("USB microphone not detected, proceeding to record video only.")
            
            # Get the current timestamp + video-only
            timestamp = datetime.now().strftime('%a%b%-d_%I-%M-%S-%p_%Y_video-only')
            
            # Remember date and time
            with open('/home/pi/Videos/datetime.txt', 'w') as f:
                f.write(timestamp)
                
            # Record Video
            video = ['bash', '/home/pi/recordvideo.sh']
            video_run = subprocess.Popen(video)
            video_run.wait()
            video_run.terminate()
            
            # Grace Period
            time.sleep(5)
            
            # Merge video only
            mergevideo = ['bash', '/home/pi/mergevid.sh']
            mergevideo_run = subprocess.Popen(mergevideo)
            mergevideo_run.wait()
            mergevideo_run.terminate()
            
            # Rename the temporary output to its timestamp
            output_file = '/home/pi/Sync/' + timestamp + '.mkv'
            os.rename('/home/pi/Videos/movie.mkv', output_file)
            
            # Remove video file
            os.remove('/home/pi/Videos/video.h264')
            os.remove('/home/pi/Videos/timestamp.pts')
            
            time.sleep(6)
            
            raise ValueError('Video-only saved.')
        
    except ValueError as e:
        print(e)
        
        # Stop raspivid
        cmd_run = subprocess.run(cmd.split(), capture_output=True, text=True)
        
        if video_run.poll() is None:
            video_run.terminate
        if audio_run.poll() is None:
            audio_run.terminate
        continue
        
    except Exception as e:
        print(e)
        time.sleep(10)
        continue
