@echo off
REM ============================================================
REM FULL PIPELINE: Fine-tune Gemma 4 E2B on Hindu Scriptures
REM ============================================================
REM Run each stage sequentially. Comment out stages to skip.
REM ============================================================

echo ============================================================
echo  HINDU SCRIPTURE FINE-TUNING PIPELINE
echo  Model: google/gemma-4-E2B-it
echo  Stages: Data Prep - CPT - SFT - DPO - GRPO - Merge - Eval
echo ============================================================
echo.

REM --- Stage 0: Generate sample data (for testing) ---
echo [STAGE 0] Generating sample datasets...
python data_processing.py generate-samples --output-dir ./data/processed
if %errorlevel% neq 0 (echo FAILED at Stage 0 & exit /b 1)
echo.

REM --- Stage 0.5: Continued Pretraining (OPTIONAL - uncomment if you have PDF corpus) ---
REM echo [STAGE 0.5] Continued Pretraining...
REM python data_processing.py process-pdfs --input-dir ./data/pdfs --output-dir ./data/processed
REM python train_cpt.py --config config.yaml
REM if %errorlevel% neq 0 (echo FAILED at CPT & exit /b 1)

REM --- Stage 1: Supervised Fine-Tuning ---
echo [STAGE 1] Supervised Fine-Tuning (SFT)...
python train_sft.py --config config.yaml
if %errorlevel% neq 0 (echo FAILED at Stage 1 SFT & exit /b 1)
echo.

REM --- Stage 2: Direct Preference Optimization ---
echo [STAGE 2] Direct Preference Optimization (DPO)...
python train_dpo.py --config config.yaml
if %errorlevel% neq 0 (echo FAILED at Stage 2 DPO & exit /b 1)
echo.

REM --- Stage 3: GRPO (Reinforcement Learning) ---
echo [STAGE 3] Group Relative Policy Optimization (GRPO)...
python train_grpo.py --config config.yaml
if %errorlevel% neq 0 (echo FAILED at Stage 3 GRPO & exit /b 1)
echo.

REM --- Stage 4: Merge all adapters ---
echo [STAGE 4] Merging all LoRA adapters...
python merge_and_export.py --config config.yaml --stage all
if %errorlevel% neq 0 (echo FAILED at Stage 4 Merge & exit /b 1)
echo.

REM --- Stage 5: Evaluation ---
echo [STAGE 5] Running evaluation...
python evaluate.py --config config.yaml --model-path ./checkpoints/merged_final --output ./eval_results.json
if %errorlevel% neq 0 (echo FAILED at Stage 5 Eval & exit /b 1)
echo.

echo ============================================================
echo  PIPELINE COMPLETE!
echo  Final model: ./checkpoints/merged_final
echo  Eval results: ./eval_results.json
echo ============================================================
