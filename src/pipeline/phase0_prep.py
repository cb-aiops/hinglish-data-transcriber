import os
from huggingface_hub import HfApi, hf_hub_download
from src.utils.audio import get_audio_duration
from src.utils.csv_helper import write_csv
from src.config import config
import pandas as pd

def run_phase0(output_file, mode="local", input_dir=None, limit=None):
    """
    Phase 0: Data Preparation
    Scans either a local directory or a Hugging Face repo for WAV files.
    """
    data = []

    if mode == "hf" and config.HF_REPO_ID:
        print(f"Running Phase 0 (HF): Scanning Hugging Face Repo {config.HF_REPO_ID}...")
        api = HfApi(token=config.HF_TOKEN)
        # List files in the repo
        files = api.list_repo_files(repo_id=config.HF_REPO_ID, repo_type="dataset")
        wav_files = [f for f in files if f.lower().endswith(".wav")]
        
        if limit:
            wav_files = wav_files[:limit]
            print(f"Limiting to first {limit} HF files.")
        
        for file_path in wav_files:
            # We don't download the whole file just to get metadata unless needed.
            # However, to get duration using the built-in wave module, we need the file locally.
            # We will download a small temp version or download it once.
            print(f"Fetching metadata for {file_path}...")
            temp_path = hf_hub_download(
                repo_id=config.HF_REPO_ID, 
                filename=file_path, 
                repo_type="dataset", 
                token=config.HF_TOKEN,
                local_dir="data/temp",
                local_dir_use_symlinks=False
            )
            duration = get_audio_duration(temp_path)
            
            data.append({
                "clip_id": os.path.splitext(os.path.basename(file_path))[0],
                "file_path": file_path, # Remote path
                "local_path": temp_path, # Temp local path
                "duration_sec": duration,
                "speaker_id": "unknown"
            })
    else:
        # Fallback to local
        input_dir = input_dir or config.RAW_DATA_DIR
        print(f"Running Phase 0 (Local): Scanning {input_dir}...")
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(".wav"):
                file_p = os.path.join(input_dir, filename)
                duration = get_audio_duration(file_p)
                data.append({
                    "clip_id": os.path.splitext(filename)[0],
                    "file_path": file_p,
                    "local_path": file_p,
                    "duration_sec": duration,
                    "speaker_id": "unknown"
                })
    
    df = pd.DataFrame(data)
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
        
    write_csv(df, output_file)
    print(f"Phase 0 complete. Found {len(data)} files. Metadata saved to {output_file}")
