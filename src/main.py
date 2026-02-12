import argparse
import sys
import os
from src.pipeline import phase0_prep, phase1_transcribe, phase2_normalize, phase3_lexicon, phase4_qa, phase5_build
from src.config import config

def main():
    parser = argparse.ArgumentParser(description="Hinglish Audio TTS Normalization Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Full Pipeline
    full_pipeline_parser = subparsers.add_parser("full-pipeline", help="Run the full pipeline (Phase 0-5)")
    full_pipeline_parser.add_argument("--version", type=str, required=True, help="Dataset version (e.g., v1)")

    # Run Phase
    run_phase_parser = subparsers.add_parser("run-phase", help="Run a specific phase")
    run_phase_parser.add_argument("phase", type=int, choices=range(6), help="Phase number (0-5)")

    # List Datasets
    subparsers.add_parser("list-datasets", help="List generated datasets")

    args = parser.parse_args()

    if args.command == "full-pipeline":
        print(f"Starting full pipeline for version: {args.version}")
        dataset_path = os.path.join(config.DATASETS_DIR, args.version)
        
        # Phase 0
        raw_metadata = os.path.join(config.PROCESSED_DATA_DIR, "metadata_raw.csv")
        phase0_prep.run_phase0(config.RAW_DATA_DIR, raw_metadata)
        
        # Phase 1
        raw_transcripts = os.path.join(config.PROCESSED_DATA_DIR, "raw_transcripts.csv")
        phase1_transcribe.run_phase1(raw_metadata, raw_transcripts)
        
        # Phase 2
        normalized_text = os.path.join(config.PROCESSED_DATA_DIR, "normalized.csv")
        # To merge results, we might need a more sophisticated merge, but for now:
        # We'll rely on the CSVs being aligned or merging them
        phase2_normalize.run_phase2(raw_transcripts, normalized_text)
        
        # Phase 3
        # Pre-merge normalized text with raw metadata for Lexicon phase
        import pandas as pd
        m_df = pd.read_csv(raw_metadata)
        t_df = pd.read_csv(raw_transcripts)
        n_df = pd.read_csv(normalized_text)
        
        merged_df = m_df.merge(t_df, on="clip_id").merge(n_df, on="clip_id")
        merged_path = os.path.join(config.PROCESSED_DATA_DIR, "merged_interim.csv")
        merged_df.to_csv(merged_path, index=False)
        
        final_processed = os.path.join(config.PROCESSED_DATA_DIR, "final_processed.csv")
        lexicon_path = os.path.join(config.LEXICON_DIR, "lexicon_v1.csv")
        phase3_lexicon.run_phase3(merged_path, final_processed, lexicon_path)
        
        # Phase 5
        phase5_build.run_phase5(final_processed, dataset_path)
        print(f"Full pipeline execution complete for {args.version}.")
    elif args.command == "run-phase":
        print(f"Starting Phase {args.phase}")
        raw_metadata = os.path.join(config.PROCESSED_DATA_DIR, "metadata_raw.csv")
        raw_transcripts = os.path.join(config.PROCESSED_DATA_DIR, "raw_transcripts.csv")
        normalized_text = os.path.join(config.PROCESSED_DATA_DIR, "normalized.csv")
        merged_path = os.path.join(config.PROCESSED_DATA_DIR, "merged_interim.csv")
        final_processed = os.path.join(config.PROCESSED_DATA_DIR, "final_processed.csv")
        lexicon_path = os.path.join(config.LEXICON_DIR, "lexicon_v1.csv")

        if args.phase == 0:
            phase0_prep.run_phase0(config.RAW_DATA_DIR, raw_metadata)
        elif args.phase == 1:
            phase1_transcribe.run_phase1(raw_metadata, raw_transcripts)
        elif args.phase == 2:
            phase2_normalize.run_phase2(raw_transcripts, normalized_text)
        elif args.phase == 3:
            import pandas as pd
            m_df = pd.read_csv(raw_metadata)
            t_df = pd.read_csv(raw_transcripts)
            n_df = pd.read_csv(normalized_text)
            merged_df = m_df.merge(t_df, on="clip_id").merge(n_df, on="clip_id")
            merged_df.to_csv(merged_path, index=False)
            phase3_lexicon.run_phase3(merged_path, final_processed, lexicon_path)
        elif args.phase == 5:
            # Check if version was provided as an extra arg or use default
            version = "manual_run_mixed_v2"
            phase5_build.run_phase5(final_processed, os.path.join(config.DATASETS_DIR, version))
    elif args.command == "list-datasets":
        print("Listing datasets...")
        # TODO: Implement listing logic
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
