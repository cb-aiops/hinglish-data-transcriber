import pandas as pd
import re
from src.utils.csv_helper import read_csv, write_csv
import os

def run_phase3(input_csv, output_csv, lexicon_path):
    """
    Phase 3: Deterministic Lexicon Enforcement
    Replaces variants with canonical forms based on the lexicon using regex.
    """
    print(f"Running Phase 3: Enforcing lexicon from {lexicon_path}...")
    
    lexicon_df = read_csv(lexicon_path)
    # Create a mapping dictionary: variant -> canonical
    lex_map = dict(zip(lexicon_df["variant"], lexicon_df["canonical"]))
    
    df = read_csv(input_csv)
    
    def apply_lexicon(text):
        # Sort variants by length descending to match longest phrases first
        for variant in sorted(lex_map.keys(), key=len, reverse=True):
            # Use regex for word boundaries to avoid partial matches
            pattern = re.compile(rf'\b{re.escape(variant)}\b', re.IGNORECASE)
            text = pattern.sub(lex_map[variant], text)
        return text

    df["text_train"] = df["text_normalized"].apply(apply_lexicon)
    
    write_csv(df, output_csv)
    print(f"Phase 3 complete. Final training text saved to {output_csv}")
