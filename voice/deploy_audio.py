import os
from pydub import AudioSegment

# Define source and destination directories, and overwrite flag
SOURCE_DIR = "C:/git/AliceResources/voice"
DEST_DIR = "C:/git/AliceWonderland/game/voice"
OVERWRITE = False  # Set to False to skip existing files
SAMPLE_RATE = 44100  # Configurable sample rate (44100 by default)
FORCE_MONO = True  # Force mono audio for mp3 export

# Character-specific settings
CHARACTER_SETTINGS = {
    "alice": {"gain": 5}, 
    "n": {"gain": 7},   
    "dodo": {"gain": 4},
    "mouse": {"gain": -3},
    "eaglet": {"gain": -2},
    "lory": {"gain": 3},
    "canry": {"gain": 3},
    "pigeon": {"gain": 3},
}

def get_character_settings(file_name):
    """
    Extract the character prefix from the file name and return the settings.
    Default to no gain adjustment if no specific settings are found.
    """
    # Extract prefix by removing digits and extension
    prefix = ''.join([c for c in os.path.splitext(file_name)[0] if not c.isdigit()]).rstrip('_')
    return CHARACTER_SETTINGS.get(prefix, {"gain": 0})

def convert_and_copy_audio(source_file, destination_file, gain):
    # Load audio file
    audio = AudioSegment.from_file(source_file)

    # Apply character-specific gain
    if gain != 0:
        audio = audio + gain

    # Apply sample rate and mono settings
    audio = audio.set_frame_rate(SAMPLE_RATE)
    if FORCE_MONO:
        audio = audio.set_channels(1)

    # Export the audio as mp3
    audio.export(destination_file, format="mp3")
    print(f"Converted and saved: {destination_file}")

def process_files():
    # Ensure destination directory exists
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    # Get list of .wav and .mp3 files from the source directory
    source_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(('.wav', '.mp3'))]

    # Check each file in the source directory
    for file_name in source_files:
        source_file_path = os.path.join(SOURCE_DIR, file_name)
        destination_file_name = os.path.splitext(file_name)[0] + ".mp3"
        destination_file_path = os.path.join(DEST_DIR, destination_file_name)

        # Skip file if it exists and overwrite is False
        if not OVERWRITE and os.path.exists(destination_file_path):
            print(f"Skipping existing file: {destination_file_path}")
            continue

        # Get character-specific settings
        settings = get_character_settings(file_name)
        gain = settings.get("gain", 0)

        # Convert and copy the file to the destination directory
        convert_and_copy_audio(source_file_path, destination_file_path, gain)

if __name__ == "__main__":
    process_files()
