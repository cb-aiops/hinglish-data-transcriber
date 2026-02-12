from groq import Groq
import pandas as pd
from src.utils.csv_helper import read_csv, write_csv
from src.config import config
import os

def run_phase2(input_csv, output_csv):
    """
    Phase 2: LLM Script Normalization
    Converts raw transcripts into Roman Hinglish using Groq API.
    """
    print(f"Running Phase 2: Normalizing transcripts via Groq ({config.GROQ_MODEL})...")
    
    if not config.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
        
    client = Groq(api_key=config.GROQ_API_KEY)
    df = read_csv(input_csv)
    
    system_prompt = (
        "You are a linguistic expert specializing in Hinglish. "
        "Your task is to normalize raw Hinglish ASR transcripts into a clean mixed-script format. "
        "Rules:\n"
        "1. No translation. Keep the meaning exactly the same.\n"
        "2. Keep Hindi words in Devanagari script (e.g., 'आज', 'नमस्ते').\n"
        "3. Convert English words and technical terms to standard English Latin script (e.g., 'video', 'CNN', 'Convolutional Neural Network').\n"
        "4. If an English word is written in Devanagari (e.g., 'वीडियो'), change it to Latin script ('video').\n"
        "5. Use numerals for numbers (e.g., '3', '10').\n"
        "6. Output ONLY the normalized text, no explanations."
    )
    
    normalized_results = []
    for _, row in df.iterrows():
        clip_id = row["clip_id"]
        raw_text = row["raw_text"]
        
        print(f"Normalizing {clip_id}...")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            model=config.GROQ_MODEL,
        )
        
        normalized_text = response.choices[0].message.content.strip()
        normalized_results.append({
            "clip_id": clip_id,
            "text_normalized": normalized_text
        })
        
    normalized_df = pd.DataFrame(normalized_results)
    write_csv(normalized_df, output_csv)
    print(f"Phase 2 complete. Normalized text saved to {output_csv}")
