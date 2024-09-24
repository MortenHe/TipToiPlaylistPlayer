import os
import re
import yaml

# Define the path to the audio folder and the output YAML file
audio_folder = r"C:\Apache24\htdocs\MortenHe\TipToiPlaylistPlayer\audio"  # Update to your actual audio folder
yaml_output_path = r"C:\Apache24\htdocs\MortenHe\TipToiPlaylistPlayer\Songs.yaml"

# Regular expression to match "XX - songname.wav" pattern
pattern = re.compile(r"^\d{2} - .+\.wav$")

# Get all wav files in the audio folder that match the pattern
wav_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav') and pattern.match(f)]

# Sort wav files by name
wav_files.sort()

# Initialize the YAML structure
yaml_content = {
    'product-id': 998,
    'comment': "Musikplayer von Martin Helfer für Laila Helfer",
    'welcome': 'start',
    'gme-lang': 'GERMAN',
    'media-path': 'Audio/%s',
    'scripts': {}
}

# Add dynamic script values using the song title
for i, file in enumerate(wav_files, start=1):
    # Get the song title from the filename
    song_title = file.split(" - ", 1)[1].rsplit('.', 1)[0]  # Strip the .wav extension
    key_name = f"{i:02d} - {song_title}"
    yaml_content['scripts'][key_name] = [f'P("{key_name}")']

# Write the YAML content to a file
with open(yaml_output_path, 'w', encoding='utf-8') as yaml_file:
    yaml.dump(yaml_content, yaml_file, allow_unicode=True, sort_keys=False)

print(f"YAML file generated at {yaml_output_path}")
