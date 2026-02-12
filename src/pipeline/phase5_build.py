import os
import shutil
import pandas as pd
from src.utils.csv_helper import read_csv, write_csv

def run_phase5(input_csv, output_dir):
    """
    Phase 5: Final Dataset Structure
    Assembles the final dataset with audio and metadata.
    """
    print(f"Running Phase 5: Building final dataset in {output_dir}...")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    audio_out_dir = os.path.join(output_dir, "audio")
    os.makedirs(audio_out_dir, exist_ok=True)
    
    df = read_csv(input_csv)
    
    # 1. Copy audio files
    for _, row in df.iterrows():
        src_path = row["file_path"]
        dest_path = os.path.join(audio_out_dir, os.path.basename(src_path))
        shutil.copy2(src_path, dest_path)
    
    # 2. Final metadata columns
    # We need to merge metadata_raw with the latest processed text
    # Assuming input_csv already has everything we need to keep
    # PRD columns: clip_id | file_path | text_train | text_raw | speaker | duration
    
    final_df = df.copy()
    # Update file paths to be relative to the dataset folder
    final_df["file_path"] = final_df["file_path"].apply(lambda x: os.path.join("audio", os.path.basename(x)))
    
    metadata_path = os.path.join(output_dir, "metadata.csv")
    write_csv(final_df, metadata_path)
    print(f"Phase 5 complete. Dataset ready at {output_dir}")
