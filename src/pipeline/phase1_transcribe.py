import whisper
import pandas as pd
from src.utils.csv_helper import read_csv, write_csv
from src.config import config
import os

def run_phase1(input_csv, output_csv):
    """
    Phase 1: Transcription
    Uses Whisper to transcribe audio files listed in input_csv.
    """
    print(f"Running Phase 1: Transcribing audio using Whisper ({config.WHISPER_MODEL})...")
    
    df = read_csv(input_csv)
    model = whisper.load_model(config.WHISPER_MODEL)
    
    results = []
    for _, row in df.iterrows():
        clip_id = row["clip_id"]
        file_path = row["file_path"]
        
        print(f"Transcribing {clip_id}...")
        result = model.transcribe(file_path, language="hi", task="transcribe")
        results.append({
            "clip_id": clip_id,
            "raw_text": result["text"].strip()
        })
        
    results_df = pd.DataFrame(results)
    write_csv(results_df, output_csv)
    print(f"Phase 1 complete. Transcripts saved to {output_csv}")
