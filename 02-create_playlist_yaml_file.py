import os
import yaml
import re

# Define the path to the audio folder and the output YAML file
audio_folder = r"audio"  # Update to your actual folder containing the WAV files
yaml_output_path = r"Laila.yaml"

# Regex pattern to match the files with the format 'XX - Name.wav'
pattern = re.compile(r"^\d{2} - (.+)\.wav$")

# Get all wav files in the source folder that match the pattern
wav_files = [f for f in os.listdir(audio_folder) if pattern.match(f)]

# Function to extract the song title from the file name
def get_song_title(file_name):
    return pattern.match(file_name).group(1).strip()

# Create a list of song titles with their XX prefix
song_titles = [(f[:2], get_song_title(f)) for f in wav_files]

# Sort the song titles by the two-digit prefix (XX)
song_titles.sort(key=lambda x: x[0])

# Initialize the YAML structure with static values
yaml_content = {
    'product-id': 997,
    'welcome': 'start',
    'gme-lang': 'GERMAN',
    'media-path': 'Audio/%s',
    'init': '$counter:=1',
    'scripts': {}
}

# Add dynamic song scripts for all matching songs
for index, (prefix, song) in enumerate(song_titles, start=1):
    song_key = f"{prefix} - {song}"
    yaml_content['scripts'][song_key] = [
        f"$counter==1? $pos1:={index} J(selected) P(s)",
        f"$counter==2? $pos2:={index} J(selected) P(s)",
        f"$counter==3? $pos3:={index} J(selected) P(s)",
        f"$counter==4? $pos4:={index} J(selected) P(s)",
        f"$counter==5? $pos5:={index} J(selected) P(s)",
        f"$counter==6? $pos6:={index} J(selected) P(s)",
        f"$counter==7? $pos7:={index} J(selected) P(s)",
        f"$counter==8? $pos8:={index} J(selected) P(s)",
        "J(check_limit) P(s)"
    ]

# Add play_songs dynamic part for 8 songs
play_songs_script = []
for i in range(1, 9):  # Only allow up to 8 songs to be played in a setlist
    for j in range(1, len(song_titles) + 1):  # Iterate over all matched songs
        play_songs_script.append(f"$counter=={i}? $pos{i}=={j}? P(\"{song_titles[j-1][0]} - {song_titles[j-1][1]}\") J(next) P(s)")

yaml_content['scripts']['play_songs'] = play_songs_script + ["J(reset) P(s)"]

# Add the static parts in the 'scripts' block
yaml_content['scripts'].update({
    'check_limit': [
        "$counter==9? P(playlist_full) P(s)"
    ],
    'reset': [
        "$counter:=1 $pos1:=0 $pos2:=0 $pos3:=0 $pos4:=0 $pos5:=0 J(reset2) P(s)"
    ],
    'reset2': [
        "$pos6:=0 $pos7:=0 $pos8:=0 P(done)"
    ],
    'selected': [
        "$counter+=1 P(song_selected) J(check_limit) P(s)"
    ],
    'playback': [
        "$counter:=1 J(play_songs) P(s)"
    ],
    'next': [
        "$counter+=1 J(play_songs) P(s)"
    ]
})

# Write the YAML content to a file
with open(yaml_output_path, 'w', encoding='utf-8') as yaml_file:
    yaml.dump(yaml_content, yaml_file, allow_unicode=True, sort_keys=False)

print(f"YAML file generated at {yaml_output_path}")
