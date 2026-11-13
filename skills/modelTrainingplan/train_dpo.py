"""
============================================================
STAGE 2: DIRECT PREFERENCE OPTIMIZATION (DPO)
============================================================
Aligns the SFT model to prefer accurate, well-cited, and
respectful answers over shallow or incorrect responses.

Pipeline:
1. Load base model + merge SFT LoRA adapters
2. Apply new LoRA adapters for DPO training
3. Train with preference pairs (chosen vs rejected)

Usage:
    python train_dpo.py --config config.yaml
    
    # Multi-GPU:
    accelerate launch train_dpo.py --config config.yaml
============================================================
"""

import argparse
import os
from pathlib import Path

import torch
import yaml
from datasets import load_dataset
from peft import LoraConfig, PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer, DPOConfig


def load_config(config_path: str) -> dict:
    """Load YAML configuration."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_sft_model(cfg: dict):
    """
    Load base model and merge SFT LoRA adapters.
    Returns the merged model ready for DPO training.
    """
    model_name = cfg["model"]["name"]
    sft_path = cfg["output"]["sft_dir"]
    
    print(f"  Loading base model: {model_name}")
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=cfg["model"].get("trust_remote_code", True),
    )
    
    # Check if SFT checkpoint exists and merge
    if Path(sft_path).exists() and (Path(sft_path) / "adapter_config.json").exists():
        print(f"  Loading SFT LoRA from: {sft_path}")
        model = PeftModel.from_pretrained(base_model, sft_path)
        print("  Merging SFT LoRA into base model...")
        model = model.merge_and_unload()
    else:
        print(f"  WARNING: No SFT checkpoint found at {sft_path}")
        print("  Training DPO directly on base model.")
        model = base_model
    
    return model


def main():
    parser = argparse.ArgumentParser(description="DPO Training for Hindu Scriptures")
    parser.add_argument("--config", type=str, default="config.yaml", help="Path to config file")
    parser.add_argument("--resume", type=str, default=None, help="Resume from checkpoint")
    parser.add_argument("--skip-merge", action="store_true", help="Skip SFT merge, use base model directly")
    args = parser.parse_args()
    
    # Load configuration
    cfg = load_config(args.config)
    dpo_cfg = cfg["dpo"]
    
    print("=" * 60)
    print("STAGE 2: DIRECT PREFERENCE OPTIMIZATION (DPO)")
    print("=" * 60)
    print(f"Model: {cfg['model']['name']}")
    print(f"SFT checkpoint: {cfg['output']['sft_dir']}")
    print(f"Output: {cfg['output']['dpo_dir']}")
    print("=" * 60)
    
    # --- Setup WandB ---
    if cfg.get("wandb", {}).get("project"):
        os.environ["WANDB_PROJECT"] = cfg["wandb"]["project"]
        if cfg["wandb"].get("entity"):
            os.environ["WANDB_ENTITY"] = cfg["wandb"]["entity"]
    
    # --- Load Dataset ---
    print("\n[1/4] Loading preference dataset...")
    train_dataset = load_dataset(
        "json",
        data_files=cfg["data"]["dpo_train"],
        split="train",
    )
    
    eval_dataset = None
    if Path(cfg["data"]["dpo_eval"]).exists():
        eval_dataset = load_dataset(
            "json",
            data_files=cfg["data"]["dpo_eval"],
            split="train",
        )
    
    print(f"  Train samples: {len(train_dataset)}")
    if eval_dataset:
        print(f"  Eval samples: {len(eval_dataset)}")
    
    # --- Load & Merge SFT Model ---
    print("\n[2/4] Loading model...")
    if args.skip_merge:
        model = cfg["model"]["name"]  # Let DPOTrainer load it
    else:
        model = load_sft_model(cfg)
    
    # --- Configure LoRA for DPO ---
    print("\n[3/4] Configuring DPO training...")
    lora_cfg = cfg["lora"]["dpo"]
    peft_config = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        target_modules=lora_cfg["target_modules"],
        lora_dropout=lora_cfg["lora_dropout"],
        task_type=lora_cfg["task_type"],
        bias="none",
    )
    print(f"  LoRA rank: {peft_config.r}")
    print(f"  LoRA alpha: {peft_config.lora_alpha}")
    print(f"  Beta (KL penalty): {dpo_cfg['beta']}")
    print(f"  Loss type: {dpo_cfg['loss_type']}")
    
    # --- Training Arguments ---
    output_dir = cfg["output"]["dpo_dir"]
    
    training_args = DPOConfig(
        output_dir=output_dir,
        num_train_epochs=dpo_cfg["num_train_epochs"],
        per_device_train_batch_size=dpo_cfg["per_device_train_batch_size"],
        gradient_accumulation_steps=dpo_cfg["gradient_accumulation_steps"],
        learning_rate=dpo_cfg["learning_rate"],
        lr_scheduler_type=dpo_cfg["lr_scheduler_type"],
        warmup_ratio=dpo_cfg["warmup_ratio"],
        weight_decay=dpo_cfg.get("weight_decay", 0.01),
        max_grad_norm=dpo_cfg.get("max_grad_norm", 1.0),
        bf16=True,
        gradient_checkpointing=True,
        max_length=cfg["model"]["max_seq_length"],
        beta=dpo_cfg["beta"],
        loss_type=[dpo_cfg["loss_type"]],
        logging_steps=dpo_cfg["logging_steps"],
        save_steps=dpo_cfg["save_steps"],
        eval_strategy="steps" if eval_dataset else "no",
        eval_steps=dpo_cfg.get("eval_steps", 200) if eval_dataset else None,
        save_total_limit=3,
        load_best_model_at_end=True if eval_dataset else False,
        report_to="wandb" if cfg.get("wandb", {}).get("project") else "none",
        run_name=f"{cfg.get('wandb', {}).get('run_name_prefix', 'dpo')}-dpo",
        dataset_num_proc=4,
    )
    
    # --- Initialize Trainer ---
    trainer = DPOTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
    )
    
    # Print info
    trainable_params = sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in trainer.model.parameters())
    print(f"  Trainable parameters: {trainable_params:,} / {total_params:,} "
          f"({100 * trainable_params / total_params:.2f}%)")
    
    # --- Train ---
    print("\n[4/4] Starting DPO training...")
    print(f"  Effective batch size: {dpo_cfg['per_device_train_batch_size'] * dpo_cfg['gradient_accumulation_steps']}")
    print(f"  Learning rate: {dpo_cfg['learning_rate']}")
    print(f"  Epochs: {dpo_cfg['num_train_epochs']}")
    print("-" * 60)
    
    trainer.train(resume_from_checkpoint=args.resume)
    
    # --- Save Final Model ---
    print("\nSaving final model...")
    trainer.save_model(output_dir)
    
    print(f"\n{'=' * 60}")
    print(f"DPO TRAINING COMPLETE")
    print(f"Model saved to: {output_dir}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
