import os
import re
import yaml

# Define the path to the audio folder and the output YAML file
audio_folder = r"audio"  # Update to your actual audio folder
yaml_output_path = r"Songs.yaml"

# Regular expression to match "XX - songname.mp3" pattern
pattern = re.compile(r"^\d{2} - .+\.mp3$")

# Get all mp3 files in the audio folder that match the pattern
mp3_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3') and pattern.match(f)]

# Sort mp3 files by name
mp3_files.sort()

# Initialize the YAML structure
yaml_content = {
    'product-id': 998,
    'welcome': 'start',
    'gme-lang': 'GERMAN',
    'media-path': 'Audio/%s',
    'scripts': {}
}

# Add dynamic script values using the song title
for i, file in enumerate(mp3_files, start=1):
    # Get the song title from the filename
    song_title = file.split(" - ", 1)[1].rsplit('.', 1)[0]  # Strip the .mp3 extension
    key_name = f"{i:02d} - {song_title}"
    yaml_content['scripts'][key_name] = [f'P("{key_name}")']

# Write the YAML content to a file
with open(yaml_output_path, 'w', encoding='utf-8') as yaml_file:
    yaml.dump(yaml_content, yaml_file, allow_unicode=True, sort_keys=False)

print(f"YAML file generated at {yaml_output_path}")
