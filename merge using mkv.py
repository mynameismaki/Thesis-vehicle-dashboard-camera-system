import os
import subprocess
import time
import shutil

# Directory where the video and audio files are located
directory = '/home/pi/Merger/'

time.sleep(10)

while True:
    try:
        
        if not os.path.exists(directory):
                os.makedirs(directory)

        # Give temporary name to the output file
        temporary_output = '/home/pi/Merger/movie.mkv'
        
        # Check if the name of the output file already exists:
        if os.path.isfile(temporary_output):
            os.remove('/home/pi/Merger/movie.mkv')
            
        # Get the list of video and audio files in the directory
        video_files = [f for f in os.listdir(directory) if f.endswith('.h264')]
        audio_files = [f for f in os.listdir(directory) if f.endswith('.wav')]
        timestamp_files = [f for f in os.listdir(directory) if f.endswith('.pts')]
        
        if video_files and audio_files and timestamp_files:
            
            # Iterate through the list of video files
            for video_file in video_files:
              # Get the name of the video file without the extension
              video_name = os.path.splitext(video_file)[0]
              # Find the corresponding audio file with the same name
              audio_file = [f for f in audio_files if f.startswith(video_name)][0]
              # Find the corresponding timestamp file with the same name
              timestamp_file = [f for f in timestamp_files if f.startswith(video_name)][0]
              # Construct the command for merging the video and audio files
              command = ['mkvmerge', '-o', temporary_output, '-A', os.path.join(directory, video_file), os.path.join(directory, audio_file), '--timecodes', '0:' + os.path.join(directory, timestamp_file)]
              
              # Finally run the command
              subprocess.run(command)
              
              # Rename the temporary output to its original file
              output_file = '/home/pi/Sync/' + video_name + '.mkv'
              os.rename(temporary_output, output_file)
              
              print(timestamp_file)
              # Delete the original video and audio files
              os.remove(os.path.join(directory, video_file))
              os.remove(os.path.join(directory, audio_file))
              os.remove(os.path.join(directory, timestamp_file))
              
              #Sleep for 5 seconds
              print("calm")
              time.sleep(5)
              
        else:
            files = os.listdir('/home/pi/Merger/') 
            # Delete all files in the merger directory
            for file in files:
                file_path = os.path.join('/home/pi/Merger/', file)
                os.remove(file_path)

            # Sleep for 10 seconds
            print("snooze")
            time.sleep(5)
    
    except Exception as e:
        print(e)
        # Delete the original video and audio files
        os.remove(os.path.join(directory, video_file))
        os.remove(os.path.join(directory, audio_file))
        os.remove(os.path.join(directory, timestamp_file))
