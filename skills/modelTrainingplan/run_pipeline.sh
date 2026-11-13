#!/bin/bash
# ============================================================
# FULL PIPELINE: Fine-tune Gemma 4 E2B on Hindu Scriptures
# ============================================================
# Run each stage sequentially. Comment out stages to skip.
# For multi-GPU, replace 'python' with 'accelerate launch'
# ============================================================

set -e  # Exit on error

echo "============================================================"
echo " HINDU SCRIPTURE FINE-TUNING PIPELINE"
echo " Model: google/gemma-4-E2B-it"
echo " Stages: Data Prep → CPT → SFT → DPO → GRPO → Merge → Eval"
echo "============================================================"
echo ""

# --- Stage 0: Generate sample data (for testing) ---
echo "[STAGE 0] Generating sample datasets..."
python data_processing.py generate-samples --output-dir ./data/processed
echo ""

# --- Stage 0.5: Continued Pretraining (OPTIONAL) ---
# Uncomment if you have PDF corpus in ./data/pdfs/
# echo "[STAGE 0.5] Processing PDFs..."
# python data_processing.py process-pdfs --input-dir ./data/pdfs --output-dir ./data/processed
# echo "[STAGE 0.5] Continued Pretraining..."
# python train_cpt.py --config config.yaml

# --- Stage 1: Supervised Fine-Tuning ---
echo "[STAGE 1] Supervised Fine-Tuning (SFT)..."
python train_sft.py --config config.yaml
echo ""

# --- Stage 2: Direct Preference Optimization ---
echo "[STAGE 2] Direct Preference Optimization (DPO)..."
python train_dpo.py --config config.yaml
echo ""

# --- Stage 3: GRPO (Reinforcement Learning) ---
echo "[STAGE 3] Group Relative Policy Optimization (GRPO)..."
python train_grpo.py --config config.yaml
echo ""

# --- Stage 4: Merge all adapters ---
echo "[STAGE 4] Merging all LoRA adapters..."
python merge_and_export.py --config config.yaml --stage all
echo ""

# --- Stage 5: Evaluation ---
echo "[STAGE 5] Running evaluation..."
python evaluate.py --config config.yaml --model-path ./checkpoints/merged_final --output ./eval_results.json
echo ""

echo "============================================================"
echo " PIPELINE COMPLETE!"
echo " Final model: ./checkpoints/merged_final"
echo " Eval results: ./eval_results.json"
echo "============================================================"
