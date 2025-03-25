import os
import re
from pydub import AudioSegment

# Define source and destination directories, and overwrite flag
SOURCE_DIR = "C:/git/AliceResources/voice"
DEST_DIR = "C:/git/AliceWonderland/game/voice"
#SOURCE_DIR = "C:/Users/Felix/Documents/git/alice/AliceResources/voice"
#DEST_DIR = "C:/Users/Felix/Documents/git/alice/AliceInWonderland/game/voice"
OVERWRITE = False  # Set to False to skip existing files
SAMPLE_RATE = 44100  # Configurable sample rate (44100 by default)
FORCE_MONO = True  # Force mono audio for mp3 export

# Character-specific settings
CHARACTER_SETTINGS = {
    "alice": {
        "gain": 3,
        "filters": [
            {"range": "84-136", "gain": 6},
            {"range": "375-386", "gain": 0},
            {"range": "30-83", "gain": 0}
        ]
    }, 
    "n": {"gain": 8},   
    "dodo": {"gain": 7},
    "mouse": {"gain": -2},
    "eaglet": {"gain": -2},
    "lory": {"gain": 4},
    "canary": {"gain": 8},
    "magpie": {"gain": 2},
    "pigeon": {"gain": 11},
    "old_crab": {"gain": 6},
    "duchess": {
        "gain": 6,
        "filters": [
            {"range": "1-1", "gain": 2},
        ]},
    "caterpillar": {"gain": 11},
    "mock": {"gain": -5},
    "frogfoot": {"gain": 7},
    "hatter": {"gain": 6},
    "dormouse": {"gain": 7},
    "na": {"gain": 7},
    "sister": {"gain": 5},
    "soldiers": {"gain": -4},
    "gryphon": {"gain": 2},
    "rabbit": {"gain": 2},
    "bill": {"gain": 2},
    "cat": {"gain": 1},
    "two": {"gain": 2},
}

def matches_range(number_range, file_name):
    """
    Check if the numeric part of the file name matches the specified range.
    Supports ranges like 1-57 or 001-057.
    """
    match = re.search(r'(\d+)', file_name)
    if not match:
        return False

    file_number = int(match.group(1))
    range_match = re.match(r'(\d+)-(\d+)', number_range)
    if not range_match:
        return False

    start, end = map(int, range_match.groups())
    return start <= file_number <= end

def get_character_settings(file_name):
    """
    Extract the character prefix from the file name and return the settings.
    Use number ranges to determine specific gains.
    """
    prefix = ''.join([c for c in os.path.splitext(file_name)[0] if not c.isdigit()]).rstrip('_')
    settings = CHARACTER_SETTINGS.get(prefix, {"gain": 0})

    # Check for specific filters
    filters = settings.get("filters", [])
    for filter_entry in filters:
        number_range = filter_entry.get("range")
        gain = filter_entry.get("gain", settings["gain"])
        if matches_range(number_range, file_name):
            return {"gain": gain}

    # Default gain if no filters match
    return {"gain": settings["gain"]}

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
