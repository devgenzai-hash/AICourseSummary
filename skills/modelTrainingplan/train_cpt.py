"""
============================================================
CONTINUED PRETRAINING (CPT) - Optional Stage 0
============================================================
Injects domain-specific vocabulary (Sanskrit terms, verse
structures, philosophical concepts) into the model before
instruction tuning.

This is optional but recommended when:
- Your scripture data contains rare Sanskrit terminology
- The base model's tokenizer fragments Devanagari heavily
- You have a large raw text corpus (>500MB)

Usage:
    python train_cpt.py --config config.yaml
============================================================
"""

import argparse
import os
from pathlib import Path

import torch
import yaml
from datasets import load_dataset
from peft import LoraConfig
from transformers import BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Continued Pretraining on Scripture Corpus")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--corpus", type=str, default=None, help="Override corpus path")
    args = parser.parse_args()
    
    cfg = load_config(args.config)
    cpt_cfg = cfg["cpt"]
    model_name = cfg["model"]["name"]
    
    print("=" * 60)
    print("STAGE 0: CONTINUED PRETRAINING (CPT)")
    print("=" * 60)
    print(f"Model: {model_name}")
    print(f"Purpose: Inject Sanskrit/Hindu scripture vocabulary")
    print("=" * 60)
    
    # --- Setup WandB ---
    if cfg.get("wandb", {}).get("project"):
        os.environ["WANDB_PROJECT"] = cfg["wandb"]["project"]
    
    # --- Load Corpus ---
    corpus_path = args.corpus or str(Path(cfg["data"]["processed_dir"]) / "corpus_chunks.jsonl")
    
    if not Path(corpus_path).exists():
        print(f"\nERROR: Corpus file not found: {corpus_path}")
        print("Run first: python data_processing.py process-pdfs --input-dir ./data/pdfs --output-dir ./data/processed")
        return
    
    print(f"\nLoading corpus: {corpus_path}")
    dataset = load_dataset("json", data_files=corpus_path, split="train")
    print(f"  Samples: {len(dataset)}")
    
    # --- Quantization ---
    quant_cfg = cfg["quantization"]
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=quant_cfg["load_in_4bit"],
        bnb_4bit_quant_type=quant_cfg["bnb_4bit_quant_type"],
        bnb_4bit_compute_dtype=getattr(torch, quant_cfg["bnb_4bit_compute_dtype"]),
        bnb_4bit_use_double_quant=quant_cfg["bnb_4bit_use_double_quant"],
    )
    
    # --- LoRA (same as SFT but with wider coverage) ---
    lora_cfg = cfg["lora"]["sft"]
    peft_config = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        target_modules=lora_cfg["target_modules"],
        lora_dropout=lora_cfg["lora_dropout"],
        task_type=lora_cfg["task_type"],
        bias="none",
    )
    
    # --- Training ---
    output_dir = cfg["output"]["cpt_dir"]
    
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=cpt_cfg["num_train_epochs"],
        per_device_train_batch_size=cpt_cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=cpt_cfg["gradient_accumulation_steps"],
        learning_rate=cpt_cfg["learning_rate"],
        lr_scheduler_type=cpt_cfg["lr_scheduler_type"],
        warmup_steps=cpt_cfg["warmup_steps"],
        bf16=True,
        gradient_checkpointing=True,
        max_length=cfg["model"]["max_seq_length"],
        packing=cpt_cfg.get("packing", True),  # Pack sequences for efficiency
        logging_steps=10,
        save_steps=500,
        save_total_limit=2,
        report_to="wandb" if cfg.get("wandb", {}).get("project") else "none",
        run_name=f"{cfg.get('wandb', {}).get('run_name_prefix', 'cpt')}-cpt",
        model_init_kwargs={
            "quantization_config": bnb_config,
            "torch_dtype": torch.bfloat16,
            "trust_remote_code": cfg["model"].get("trust_remote_code", True),
        },
    )
    
    trainer = SFTTrainer(
        model=model_name,
        args=training_args,
        train_dataset=dataset,
        peft_config=peft_config,
    )
    
    print(f"\nStarting continued pretraining...")
    print(f"  Epochs: {cpt_cfg['num_train_epochs']}")
    print(f"  Learning rate: {cpt_cfg['learning_rate']}")
    print(f"  Packing: {cpt_cfg.get('packing', True)}")
    print("-" * 60)
    
    trainer.train()
    trainer.save_model(output_dir)
    
    print(f"\n{'=' * 60}")
    print(f"CPT COMPLETE — Model saved to: {output_dir}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
