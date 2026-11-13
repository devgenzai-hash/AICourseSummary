# Fine-Tuning Gemma 4 E2B on Hindu Scriptures

End-to-end pipeline for fine-tuning `google/gemma-4-E2B-it` on Hindu scriptures in Hindi, Sanskrit, and English.

## Pipeline Overview

```
PDF Scriptures → Data Processing → CPT (optional) → SFT → DPO → GRPO → Merged Model
```

| Stage | Script | Purpose |
|-------|--------|---------|
| Data Prep | `data_processing.py` | PDF extraction, OCR, cleaning, formatting |
| CPT | `train_cpt.py` | Inject domain vocabulary (optional) |
| SFT | `train_sft.py` | Instruction following on scripture Q&A |
| DPO | `train_dpo.py` | Preference alignment (accurate > shallow) |
| GRPO | `train_grpo.py` | RL with verifiable scripture rewards |
| Merge | `merge_and_export.py` | Combine all LoRA adapters |
| Eval | `evaluate.py` | Verse accuracy, citation rate, quality |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data (for testing pipeline)
python data_processing.py generate-samples --output-dir ./data/processed

# 3. Run full pipeline
python train_sft.py --config config.yaml
python train_dpo.py --config config.yaml
python train_grpo.py --config config.yaml
python merge_and_export.py --config config.yaml --stage all
python evaluate.py --config config.yaml --model-path ./checkpoints/merged_final
```

Or use the batch script:
```bash
# Windows
run_pipeline.bat

# Linux/Mac
chmod +x run_pipeline.sh && ./run_pipeline.sh
```

## Hardware Requirements

| Setup | GPU | Stages Supported |
|-------|-----|-----------------|
| Minimum | 1x RTX 4090 (24GB) | SFT + DPO (QLoRA) |
| Recommended | 1x A100 (40GB) | All stages |
| Ideal | 2x A100 (80GB) | All + vLLM for GRPO |

## Project Structure

```
modelTrainingplan/
├── config.yaml              # Central configuration
├── requirements.txt         # Python dependencies
├── data_processing.py       # PDF → training data pipeline
├── train_cpt.py            # Stage 0: Continued pretraining
├── train_sft.py            # Stage 1: Supervised fine-tuning
├── train_dpo.py            # Stage 2: Preference optimization
├── train_grpo.py           # Stage 3: Reinforcement learning
├── merge_and_export.py     # Merge LoRA + export
├── evaluate.py             # Evaluation suite
├── accelerate_config.yaml  # Multi-GPU config (DeepSpeed ZeRO-3)
├── run_pipeline.bat        # Windows batch runner
└── run_pipeline.sh         # Linux/Mac runner
```

## Data Preparation

### Processing Your PDFs

Place PDF files in `./data/pdfs/` then run:
```bash
python data_processing.py process-pdfs --input-dir ./data/pdfs --output-dir ./data/processed
```

This handles:
- Digital PDFs (PyMuPDF text extraction)
- Scanned PDFs (Tesseract OCR with Hindi/Sanskrit)
- Unicode normalization for Devanagari
- Chunking into training segments

### Required Data Formats

**SFT** (instruction tuning):
```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

**DPO** (preference pairs):
```json
{"prompt": [{"role": "user", "content": "..."}], "chosen": [{"role": "assistant", "content": "..."}], "rejected": [{"role": "assistant", "content": "..."}]}
```

**GRPO** (RL prompts):
```json
{"prompt": [{"role": "user", "content": "..."}], "ground_truth": "..."}
```

## Configuration

All hyperparameters are in `config.yaml`. Key settings:

| Parameter | SFT | DPO | GRPO |
|-----------|-----|-----|------|
| Learning Rate | 2e-4 | 5e-6 | 1e-6 |
| LoRA Rank | 64 | 32 | 32 |
| Batch Size (eff.) | 32 | 32 | 16 |
| Epochs | 3 | 1 | 1 |

## Multi-GPU Training

```bash
# Configure accelerate (one-time)
accelerate config

# Launch with DeepSpeed ZeRO-3
accelerate launch --config_file accelerate_config.yaml train_sft.py --config config.yaml
```

## WandB Logging

Set your WandB credentials:
```bash
wandb login
```

Then ensure `wandb.project` is set in `config.yaml`.
