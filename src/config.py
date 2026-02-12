import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"
    DATASETS_DIR = "data/datasets"
    LEXICON_DIR = "lexicon"
    
    WHISPER_MODEL = "small"
    
    # API Keys (loaded from environment)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "openai/gpt-oss-120b"
    
    # Hugging Face Settings
    HF_TOKEN = os.getenv("HF_TOKEN")
    HF_REPO_ID = os.getenv("HF_REPO_ID") # e.g. "username/dataset-name"

config = Config()
