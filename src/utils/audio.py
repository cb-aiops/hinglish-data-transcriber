import wave
import os

def get_audio_duration(file_path):
    """Returns the duration of a WAV file in seconds using the built-in wave module."""
    try:
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0.0

def validate_audio_file(file_path):
    """Checks if the file is a valid WAV and within the expected duration (6-30s)."""
    if not file_path.lower().endswith(".wav"):
        return False
    
    duration = get_audio_duration(file_path)
    return 6.0 <= duration <= 30.0
