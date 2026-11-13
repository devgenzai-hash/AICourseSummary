"""
============================================================
STAGE 1: SUPERVISED FINE-TUNING (SFT)
============================================================
Fine-tunes Gemma 4 E2B on Hindu scripture instruction data
using QLoRA for memory efficiency.

Features:
- 4-bit quantization (NF4) for base model
- LoRA adapters on attention + MLP layers
- Assistant-only loss (only trains on responses)
- Gradient checkpointing for memory savings
- WandB logging

Usage:
    python train_sft.py --config config.yaml
    
    # Multi-GPU with accelerate:
    accelerate launch train_sft.py --config config.yaml
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
    """Load YAML configuration."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_bnb_config(cfg: dict) -> BitsAndBytesConfig:
    """Create BitsAndBytes quantization config."""
    quant_cfg = cfg["quantization"]
    return BitsAndBytesConfig(
        load_in_4bit=quant_cfg["load_in_4bit"],
        bnb_4bit_quant_type=quant_cfg["bnb_4bit_quant_type"],
        bnb_4bit_compute_dtype=getattr(torch, quant_cfg["bnb_4bit_compute_dtype"]),
        bnb_4bit_use_double_quant=quant_cfg["bnb_4bit_use_double_quant"],
    )


def get_lora_config(cfg: dict, stage: str = "sft") -> LoraConfig:
    """Create LoRA config for the specified stage."""
    lora_cfg = cfg["lora"][stage]
    return LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        target_modules=lora_cfg["target_modules"],
        lora_dropout=lora_cfg["lora_dropout"],
        task_type=lora_cfg["task_type"],
        bias="none",
    )


def main():
    parser = argparse.ArgumentParser(description="SFT Training for Hindu Scriptures")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config file")
    parser.add_argument("--resume", type=str, default=None, help="Resume from checkpoint path")
    args = parser.parse_args()
    
    # Load configuration
    cfg = load_config(args.config)
    sft_cfg = cfg["sft"]
    model_name = cfg["model"]["name"]
    
    print("=" * 60)
    print("STAGE 1: SUPERVISED FINE-TUNING (SFT)")
    print("=" * 60)
    print(f"Model: {model_name}")
    print(f"Output: {cfg['output']['sft_dir']}")
    print(f"Train data: {cfg['data']['sft_train']}")
    print("=" * 60)
    
    # --- Setup WandB ---
    if cfg.get("wandb", {}).get("project"):
        os.environ["WANDB_PROJECT"] = cfg["wandb"]["project"]
        if cfg["wandb"].get("entity"):
            os.environ["WANDB_ENTITY"] = cfg["wandb"]["entity"]
    
    # --- Load Dataset ---
    print("\n[1/4] Loading dataset...")
    train_dataset = load_dataset(
        "json", 
        data_files=cfg["data"]["sft_train"], 
        split="train"
    )
    
    eval_dataset = None
    if Path(cfg["data"]["sft_eval"]).exists():
        eval_dataset = load_dataset(
            "json", 
            data_files=cfg["data"]["sft_eval"], 
            split="train"
        )
    
    print(f"  Train samples: {len(train_dataset)}")
    if eval_dataset:
        print(f"  Eval samples: {len(eval_dataset)}")
    
    # --- Configure Quantization ---
    print("\n[2/4] Configuring model (QLoRA 4-bit)...")
    bnb_config = get_bnb_config(cfg)
    
    # --- Configure LoRA ---
    peft_config = get_lora_config(cfg, stage="sft")
    print(f"  LoRA rank: {peft_config.r}")
    print(f"  LoRA alpha: {peft_config.lora_alpha}")
    print(f"  Target modules: {peft_config.target_modules}")
    
    # --- Training Arguments ---
    print("\n[3/4] Setting up trainer...")
    output_dir = cfg["output"]["sft_dir"]
    
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=sft_cfg["num_train_epochs"],
        per_device_train_batch_size=sft_cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=sft_cfg["gradient_accumulation_steps"],
        learning_rate=sft_cfg["learning_rate"],
        lr_scheduler_type=sft_cfg["lr_scheduler_type"],
        warmup_ratio=sft_cfg["warmup_ratio"],
        weight_decay=sft_cfg.get("weight_decay", 0.01),
        max_grad_norm=sft_cfg.get("max_grad_norm", 1.0),
        bf16=True,
        gradient_checkpointing=True,
        max_length=cfg["model"]["max_seq_length"],
        logging_steps=sft_cfg["logging_steps"],
        save_steps=sft_cfg["save_steps"],
        eval_strategy="steps" if eval_dataset else "no",
        eval_steps=sft_cfg.get("eval_steps", 500) if eval_dataset else None,
        save_total_limit=3,
        load_best_model_at_end=True if eval_dataset else False,
        report_to="wandb" if cfg.get("wandb", {}).get("project") else "none",
        run_name=f"{cfg.get('wandb', {}).get('run_name_prefix', 'sft')}-sft",
        assistant_only_loss=sft_cfg.get("assistant_only_loss", True),
        packing=sft_cfg.get("packing", False),
        dataset_num_proc=4,
        # Model loading kwargs
        model_init_kwargs={
            "quantization_config": bnb_config,
            "torch_dtype": torch.bfloat16,
            "trust_remote_code": cfg["model"].get("trust_remote_code", True),
        },
    )
    
    # --- Initialize Trainer ---
    trainer = SFTTrainer(
        model=model_name,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
    )
    
    # Print trainable parameters
    trainable_params = sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in trainer.model.parameters())
    print(f"  Trainable parameters: {trainable_params:,} / {total_params:,} "
          f"({100 * trainable_params / total_params:.2f}%)")
    
    # --- Train ---
    print("\n[4/4] Starting training...")
    print(f"  Effective batch size: {sft_cfg['per_device_train_batch_size'] * sft_cfg['gradient_accumulation_steps']}")
    print(f"  Learning rate: {sft_cfg['learning_rate']}")
    print(f"  Epochs: {sft_cfg['num_train_epochs']}")
    print("-" * 60)
    
    trainer.train(resume_from_checkpoint=args.resume)
    
    # --- Save Final Model ---
    print("\n Saving final model...")
    trainer.save_model(output_dir)
    
    print(f"\n{'=' * 60}")
    print(f"SFT TRAINING COMPLETE")
    print(f"Model saved to: {output_dir}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
