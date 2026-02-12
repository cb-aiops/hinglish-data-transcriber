import os
from src.utils.audio import get_audio_duration, validate_audio_file
from src.utils.csv_helper import write_csv
import pandas as pd

def run_phase0(input_dir, output_file):
    """
    Phase 0: Data Preparation
    Scans the input directory for WAV files and creates metadata_raw.csv.
    """
    print(f"Running Phase 0: Scanning {input_dir}...")
    
    data = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            file_path = os.path.join(input_dir, filename)
            duration = get_audio_duration(file_path)
            
            # For simplicity, we assume speaker_id is unknown or extracted from filename
            speaker_id = "unknown" 
            
            data.append({
                "clip_id": os.path.splitext(filename)[0],
                "file_path": file_path,
                "duration_sec": duration,
                "speaker_id": speaker_id
            })
    
    df = pd.DataFrame(data)
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
        
    write_csv(df, output_file)
    print(f"Phase 0 complete. Found {len(data)} files. Metadata saved to {output_file}")
