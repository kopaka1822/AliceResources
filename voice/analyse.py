import os
import numpy as np
from pydub import AudioSegment

# Configuration
SOURCE_DIR = "C:/git/AliceResources/voice"
REF_VOICE = "mouse"

def analyze_audio_files(source_dir, ref_voice):
    """Analyze audio files and calculate stats for volume matching."""
    character_files = {}
    reference_max_gain_linear = []

    # Group files by character prefix
    for file_name in os.listdir(source_dir):
        if file_name.endswith(".wav") or file_name.endswith(".mp3"):
            # Extract prefix (ignore numeric parts and file extension)
            prefix = ''.join([c for c in os.path.splitext(file_name)[0] if not c.isdigit()]).rstrip('_')
            file_path = os.path.join(source_dir, file_name)
            audio = AudioSegment.from_file(file_path)

            # Calculate maximum safe gain (to avoid clipping)
            peak = audio.max_dBFS
            safe_gain_dB = -peak  # Max gain in dB without clipping
            safe_gain_linear = 10 ** (safe_gain_dB / 20)  # Convert to linear scale

            if prefix == ref_voice:
                reference_max_gain_linear.append(safe_gain_linear)

            if prefix not in character_files:
                character_files[prefix] = []
            character_files[prefix].append((file_name, safe_gain_linear, safe_gain_dB, audio))

    # Calculate stats
    if not reference_max_gain_linear:
        print(f"No reference voice files found for prefix '{ref_voice}'.")
        return None

    ref_safe_gain_linear = min(reference_max_gain_linear)  # Use the lowest safe gain in linear scale
    print(f"Reference Max Safe Gain for '{ref_voice}' (Linear): {ref_safe_gain_linear:.3f}")

    results = {}
    for character, files in character_files.items():
        char_safe_gains_linear = [safe_gain for _, safe_gain, _, _ in files]

        # Calculate max safe gain for the character in linear scale
        max_safe_gain_linear = min(char_safe_gains_linear)
        max_safe_gain_dB = 20 * np.log10(max_safe_gain_linear)  # Convert to dB

        # Calculate normalization gain in linear scale
        normalization_linear = max_safe_gain_linear / ref_safe_gain_linear if ref_safe_gain_linear != 0 else 1

        # Convert the normalization gain back to dB
        normalization_dB = 20 * np.log10(normalization_linear)

        results[character] = {
            "normalization_linear": normalization_linear,
            "normalization_dB": normalization_dB,
            "max_safe_gain_linear": max_safe_gain_linear,
            "max_safe_gain_dB": max_safe_gain_dB,
        }

    return results

# Run analysis
results = analyze_audio_files(SOURCE_DIR, REF_VOICE)

# Output results
if results:
    for character, stats in results.items():
        print(f"\nCharacter: {character}")
        #print(f"  Normalization Linear (relative to reference): {stats['normalization_linear']:.3f}")
        #print(f"  Normalization dB (relative to reference): {stats['normalization_dB']:.2f} dB")
        print(f"  Max Safe Gain Linear: {stats['max_safe_gain_linear']:.3f}")
        print(f"  Max Safe Gain (non-linear dB): {stats['max_safe_gain_dB']:.2f} dB")
