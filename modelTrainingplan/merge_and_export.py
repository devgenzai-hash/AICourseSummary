"""
============================================================
MODEL MERGING & EXPORT
============================================================
Merges LoRA adapters from all training stages into a single
deployable model. Supports:
- Progressive merge (SFT → DPO → GRPO)
- Export to HuggingFace Hub
- GGUF quantization for Ollama/llama.cpp

Usage:
    # Merge all stages
    python merge_and_export.py --config config.yaml
    
    # Merge specific stage only
    python merge_and_export.py --config config.yaml --stage sft
    
    # Push to Hub
    python merge_and_export.py --config config.yaml --push-to-hub your-username/model-name
============================================================
"""

import argparse
from pathlib import Path

import torch
import yaml
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def merge_adapters(
    base_model_name: str,
    adapter_paths: list[str],
    output_dir: str,
    trust_remote_code: bool = True,
):
    """
    Progressively merge multiple LoRA adapters into the base model.
    
    Args:
        base_model_name: HuggingFace model ID or local path
        adapter_paths: List of paths to LoRA adapters (in order)
        output_dir: Where to save the merged model
        trust_remote_code: Trust remote code in model
    """
    print(f"\nLoading base model: {base_model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=trust_remote_code,
    )
    
    tokenizer = AutoTokenizer.from_pretrained(
        base_model_name,
        trust_remote_code=trust_remote_code,
    )
    
    # Merge each adapter in sequence
    for i, adapter_path in enumerate(adapter_paths):
        adapter_path = Path(adapter_path)
        if not adapter_path.exists():
            print(f"  [SKIP] Adapter not found: {adapter_path}")
            continue
        if not (adapter_path / "adapter_config.json").exists():
            print(f"  [SKIP] No adapter_config.json in: {adapter_path}")
            continue
            
        print(f"  [{i+1}/{len(adapter_paths)}] Merging adapter: {adapter_path}")
        model = PeftModel.from_pretrained(model, str(adapter_path))
        model = model.merge_and_unload()
        print(f"    Merged successfully.")
    
    # Save merged model
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nSaving merged model to: {output_path}")
    model.save_pretrained(str(output_path), safe_serialization=True)
    tokenizer.save_pretrained(str(output_path))
    
    # Print model size
    param_count = sum(p.numel() for p in model.parameters())
    size_gb = param_count * 2 / (1024**3)  # bfloat16 = 2 bytes per param
    print(f"  Parameters: {param_count:,}")
    print(f"  Size (bf16): {size_gb:.2f} GB")
    
    return model, tokenizer


def push_to_hub(model_path: str, repo_id: str, private: bool = False):
    """Push merged model to HuggingFace Hub."""
    from huggingface_hub import HfApi
    
    print(f"\nPushing to HuggingFace Hub: {repo_id}")
    
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="cpu",
    )
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    model.push_to_hub(repo_id, private=private)
    tokenizer.push_to_hub(repo_id, private=private)
    
    print(f"  Successfully pushed to: https://huggingface.co/{repo_id}")


def main():
    parser = argparse.ArgumentParser(description="Merge LoRA adapters and export model")
    parser.add_argument("--config", type=str, default="config.yaml", help="Config file path")
    parser.add_argument("--stage", type=str, default="all", 
                       choices=["sft", "dpo", "grpo", "all"],
                       help="Which stage to merge up to")
    parser.add_argument("--push-to-hub", type=str, default=None,
                       help="HuggingFace repo ID to push (e.g., 'username/model-name')")
    parser.add_argument("--private", action="store_true", help="Make Hub repo private")
    args = parser.parse_args()
    
    cfg = load_config(args.config)
    
    print("=" * 60)
    print("MODEL MERGING & EXPORT")
    print("=" * 60)
    
    # Determine which adapters to merge
    adapter_paths = []
    if args.stage in ("sft", "dpo", "grpo", "all"):
        adapter_paths.append(cfg["output"]["sft_dir"])
    if args.stage in ("dpo", "grpo", "all"):
        adapter_paths.append(cfg["output"]["dpo_dir"])
    if args.stage in ("grpo", "all"):
        adapter_paths.append(cfg["output"]["grpo_dir"])
    
    print(f"Base model: {cfg['model']['name']}")
    print(f"Adapters to merge: {len(adapter_paths)}")
    for p in adapter_paths:
        exists = "✓" if Path(p).exists() else "✗"
        print(f"  [{exists}] {p}")
    
    # Merge
    model, tokenizer = merge_adapters(
        base_model_name=cfg["model"]["name"],
        adapter_paths=adapter_paths,
        output_dir=cfg["output"]["merged_dir"],
        trust_remote_code=cfg["model"].get("trust_remote_code", True),
    )
    
    # Push to Hub if requested
    if args.push_to_hub:
        push_to_hub(cfg["output"]["merged_dir"], args.push_to_hub, private=args.private)
    
    print(f"\n{'=' * 60}")
    print(f"MERGE COMPLETE")
    print(f"Final model: {cfg['output']['merged_dir']}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
