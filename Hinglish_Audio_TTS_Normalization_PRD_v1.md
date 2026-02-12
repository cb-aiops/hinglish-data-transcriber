# PRD.md

# Project: Hinglish Audio → Clean Training Text Pipeline (Natural YouTube Dubbing)

------------------------------------------------------------------------

## 1. Executive Summary

This project builds a production-grade pipeline to convert chunked
Hinglish WAV audio files (6--30 seconds) into clean,
pronunciation-stable Roman Hinglish training text suitable for natural
YouTube dubbing voice generation.

The system will:

-   Transcribe Hinglish audio using Whisper.
-   Normalize transcripts into consistent Roman Hinglish.
-   Enforce deterministic canonical vocabulary rules.
-   Generate a structured dataset ready for TTS training.
-   Maintain reproducibility and version control.

------------------------------------------------------------------------

## 2. Problem Statement

Current ASR outputs from Whisper: - Contain inconsistent script usage
(Devanagari + Latin). - Transliterate English words into Hindi script
unpredictably. - Produce inconsistent Roman spellings when normalized. -
Create unstable input for TTS training.

We require a deterministic normalization pipeline to ensure phonetic
stability for Hinglish TTS.

------------------------------------------------------------------------

## 3. Objectives

1.  Create batch transcription pipeline.
2.  Convert raw transcripts into Roman Hinglish training format.
3.  Enforce canonical spellings for English technical terms.
4.  Enforce consistent Roman Hindi spelling policy.
5.  Enable versioned dataset generation.
6.  Minimize manual effort via structured QA sampling.

------------------------------------------------------------------------

## 4. Strategic Decision

### Training Text Format: Roman Hinglish (Mandatory)

Reason: - Stable grapheme-to-phoneme mapping. - Avoids mixed-script TTS
instability. - Improves pronunciation consistency. - Faster production
deployment.

Example:

Raw: आपकी इमेज है और थ्री है उसमें चैनल्स

Training: aapki image hai aur 3 hai usme channels

------------------------------------------------------------------------

## 5. Scope

### In Scope

-   Whisper batch transcription
-   LLM normalization layer
-   Lexicon enforcement engine
-   QA sampling system
-   Dataset builder
-   Versioning strategy

### Out of Scope

-   Fine-tuning ASR
-   TTS model training
-   Subtitle rendering system

------------------------------------------------------------------------

## 6. High-Level Architecture

Audio WAV Files\
↓\
Whisper Transcription (Raw Hindi Output)\
↓\
LLM Script Normalization\
↓\
Deterministic Lexicon Enforcement\
↓\
QA Sampling\
↓\
Final Dataset (metadata.csv + audio folder)

------------------------------------------------------------------------

## 7. Detailed Pipeline Specification

### Phase 0 -- Data Preparation

Inputs: - WAV files (6--30 sec) - Speaker metadata (if multi-speaker)

Output: metadata_raw.csv

Columns: - clip_id - file_path - duration_sec - speaker_id

------------------------------------------------------------------------

### Phase 1 -- Transcription

Tool: Whisper large-v3

Configuration: - task = transcribe - language = hi - no translation mode

Output: raw_transcripts.csv

Columns: - clip_id - raw_text - timestamps (optional)

------------------------------------------------------------------------

### Phase 2 -- LLM Script Normalization

Purpose: Convert raw transcript into Roman Hinglish without altering
meaning.

Rules: 1. No translation. 2. Hindi words → Roman Hindi. 3. English words
→ Standard English. 4. Preserve names. 5. Preserve URLs. 6. Use numerals
for numbers. 7. No paraphrasing.

------------------------------------------------------------------------

### Phase 3 -- Deterministic Lexicon Enforcement

Maintain lexicon_v1.csv

Example:

  variant    canonical
  ---------- -----------
  open ai    OpenAI
  chat gpt   ChatGPT
  cnn        CNN
  kyonki     kyunki
  hoon       hoon

System: - Replace all variants with canonical form. - Enforce casing. -
Enforce spelling consistency.

------------------------------------------------------------------------

### Phase 4 -- QA Sampling

Procedure: - Sample 10--15% clips. - Prioritize high technical density
clips. - Update lexicon if systematic drift observed. - Re-run
normalization.

Goal: Error rate \< 5%.

------------------------------------------------------------------------

### Phase 5 -- Final Dataset Structure

dataset_v1/

audio/ clip_001.wav clip_002.wav

metadata.csv

Columns:

| clip_id \| file_path \| text_train \| text_raw \| speaker \| duration
  \|

------------------------------------------------------------------------

## 8. Versioning Strategy

Each pipeline run must create:

-   dataset_v1/
-   dataset_v2/

Track: - Whisper version - Prompt version - Lexicon version - Date stamp

Never overwrite previous dataset versions.

------------------------------------------------------------------------

## 9. Quality Metrics

1.  Technical word consistency: 100%
2.  Roman Hindi spelling consistency: 100%
3.  Manual QA error rate \< 5%
4.  TTS naturalness validation pass

------------------------------------------------------------------------

## 10. Risks & Mitigation

  Risk                     Mitigation
  ------------------------ -------------------------------
  LLM hallucination        Deterministic lexicon layer
  Spelling drift           Canonical mapping enforcement
  ASR mis-hearing          QA sampling
  Multi-speaker blending   Speaker tagging

------------------------------------------------------------------------

## 11. Deliverables

1.  Whisper batch script
2.  LLM normalization module
3.  Lexicon enforcement engine
4.  QA sampling script
5.  Dataset builder script
6.  normalization_policy.md
7.  dataset_vX output

------------------------------------------------------------------------

## 12. Success Criteria

Pipeline is successful if:

-   Clean Roman Hinglish dataset generated.
-   Tech vocabulary stable.
-   No script-switch instability.
-   TTS trained on dataset produces natural YouTube-style Hinglish
    voice.

------------------------------------------------------------------------

END OF DOCUMENT
