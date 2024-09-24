import os
import re
import yaml

# Define paths
audio_folder = r"C:\Apache24\htdocs\MortenHe\TipToiPlaylistPlayer\audio"
yaml_output_path = r"C:\Apache24\htdocs\MortenHe\TipToiPlaylistPlayer\Laila.yaml"

# Regular expression to match "XX - songname.wav" pattern
pattern = re.compile(r"^\d{2} - .+\.wav$")

# Get all wav files in the audio folder that match the pattern
wav_files = [f for f in os.listdir(audio_folder) if f.endswith('.wav') and pattern.match(f)]

# Sort wav files by name
wav_files.sort()

# Initialize the YAML structure
yaml_content = {
    'product-id': 999,
    'comment': "Musikplayer von Martin Helfer für Laila Helfer",
    'welcome': 'start',
    'gme-lang': 'GERMAN',
    'media-path': 'Audio/%s',
    'init': '$div:=1 $seq:=0 $song:=0 $factor:=100',
    'scripts': {}
}

# Add dynamic set_XX values
for i, file in enumerate(wav_files, start=1):
    song_title = file.split(" - ", 1)[1].rsplit('.', 1)[0]  # Strip the .wav extension
    key_name = f"{i:02d} - {song_title}"
    seq_value = f"$seq*=$factor $seq+={i} $div*=$factor P(selected)"
    yaml_content['scripts'][key_name] = [seq_value]

# Add dynamic play_songs values
play_songs = []
for i, file in enumerate(wav_files, start=1):
    song_title = file.split(" - ", 1)[1].rsplit('.', 1)[0]
    play_songs.append(f"$song=={i}? P(\"{i:02d} - {song_title}\") J(playback)")

yaml_content['scripts']['play_songs'] = play_songs

# Add static scripts (playback, next, reset)
yaml_content['scripts'].update({
    'playback': [
        '$div==1? J(reset)',
        '$div/=$factor $song:=$seq $song/=$div $seq%=$div J(play_songs)'
    ],
    'next': [
        'J(playback)'
    ],
    'reset': [
        '$div:=1 $seq:=0 $song:=0 P(done)'
    ]
})

# Write the YAML content to a file
with open(yaml_output_path, 'w', encoding='utf-8') as yaml_file:
    yaml.dump(yaml_content, yaml_file, allow_unicode=True, sort_keys=False)

print(f"YAML file generated at {yaml_output_path}")
