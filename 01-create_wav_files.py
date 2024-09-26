import os
import re
import shutil
from pydub import AudioSegment

# Define paths
source_folder = r"audio-mp3"
destination_folder = r"audio"

# Control whether to limit the mp3 files to 3 seconds or keep original length
limit_to_3_seconds = False

# Ensure destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Remove existing MP3 files that follow the pattern 'XX - Name.mp3' from the audio folder
pattern = re.compile(r"^\d{2} - .+\.mp3$")
existing_mp3_files = [f for f in os.listdir(destination_folder) if f.endswith('.mp3') and pattern.match(f)]
for file in existing_mp3_files:
    file_path = os.path.join(destination_folder, file)
    os.remove(file_path)
    print(f"Removed: {file}")

# Get all mp3 files in the source folder
mp3_files = [f for f in os.listdir(source_folder) if f.endswith('.mp3')]

# Function to extract the song title
def get_song_title(file_name):
    return file_name.split(" - ", 1)[1].rsplit('.', 1)[0].strip()

# Create a list of tuples (new_name, full_source_path)
renamed_files = [(get_song_title(f), os.path.join(source_folder, f)) for f in mp3_files]

# Sort by the new names
renamed_files.sort(key=lambda x: x[0])

# Loop through the sorted list, rename, convert and move
for index, (song_title, source_path) in enumerate(renamed_files, start=1):
    # Create the new file name with a two-digit prefix
    new_file_name = f"{index:02d} - {song_title}.mp3"
    
    # Define the full destination path
    destination_path = os.path.join(destination_folder, new_file_name)
    
    if limit_to_3_seconds:
        # Load mp3 file
        audio = AudioSegment.from_mp3(source_path)
        
        # Shorten the audio to the first 3 seconds
        short_audio = audio[:3000]  # 3000ms = 3 seconds
        
        # Export the audio as mp3 to the destination folder
        short_audio.export(destination_path, format="mp3")
        print(f"Processed and moved: {new_file_name} (limited to 3 seconds)")
    
    else:
        # Simply copy and rename the file without reprocessing
        shutil.copy2(source_path, destination_path)
        print(f"Copied and renamed: {new_file_name}")

print("All files processed successfully.")
