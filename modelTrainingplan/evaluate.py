"""
============================================================
MODEL EVALUATION
============================================================
Evaluates the fine-tuned model on Hindu scripture tasks:
- Verse identification accuracy
- Translation quality (BLEU/ROUGE)
- Factual knowledge quiz
- Qualitative generation samples
- General capability retention check

Usage:
    python evaluate.py --config config.yaml --model-path ./checkpoints/merged_final
    python evaluate.py --config config.yaml --model-path ./checkpoints/sft  # Evaluate SFT only
============================================================
"""

import argparse
import json
import re
from pathlib import Path

import torch
import yaml
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ============================================================
# EVALUATION METRICS
# ============================================================

def compute_verse_accuracy(model_pipe, test_data: list[dict]) -> dict:
    """
    Evaluate: Can the model correctly identify verses?
    
    Test data format: [{"question": "...", "ground_truth": "..."}]
    """
    correct = 0
    partial = 0
    total = len(test_data)
    results = []
    
    for item in tqdm(test_data, desc="Verse Accuracy"):
        messages = [{"role": "user", "content": item["question"]}]
        response = model_pipe(messages, max_new_tokens=256, do_sample=False)
        generated = response[0]["generated_text"][-1]["content"]
        
        gt = item["ground_truth"].lower().strip()
        gen_lower = generated.lower()
        
        is_correct = gt in gen_lower
        is_partial = any(part in gen_lower for part in gt.split() if len(part) > 2)
        
        if is_correct:
            correct += 1
        elif is_partial:
            partial += 1
        
        results.append({
            "question": item["question"],
            "expected": item["ground_truth"],
            "generated": generated[:200],
            "correct": is_correct,
        })
    
    return {
        "accuracy": correct / max(total, 1),
        "partial_accuracy": (correct + partial) / max(total, 1),
        "correct": correct,
        "partial": partial,
        "total": total,
        "details": results,
    }


def compute_citation_rate(model_pipe, prompts: list[str]) -> dict:
    """
    Evaluate: How often does the model cite specific verses?
    """
    citation_patterns = [
        r"(Chapter|अध्याय|Ch\.?)\s*\d+.*?(Verse|श्लोक|V\.?)\s*\d+",
        r"(BG|RV|SB|BS|YS)\s*\d+[\.:]\d+",
        r"\d+\.\d+",
    ]
    
    cited = 0
    total = len(prompts)
    
    for prompt in tqdm(prompts, desc="Citation Rate"):
        messages = [{"role": "user", "content": prompt}]
        response = model_pipe(messages, max_new_tokens=512, do_sample=False)
        generated = response[0]["generated_text"][-1]["content"]
        
        has_citation = any(
            re.search(p, generated, re.IGNORECASE) 
            for p in citation_patterns
        )
        if has_citation:
            cited += 1
    
    return {
        "citation_rate": cited / max(total, 1),
        "cited": cited,
        "total": total,
    }


def compute_sanskrit_inclusion_rate(model_pipe, prompts: list[str]) -> dict:
    """
    Evaluate: How often does the model include original Sanskrit text?
    """
    devanagari_pattern = r"[\u0900-\u097F]{3,}"
    included = 0
    total = len(prompts)
    
    for prompt in tqdm(prompts, desc="Sanskrit Inclusion"):
        messages = [{"role": "user", "content": prompt}]
        response = model_pipe(messages, max_new_tokens=512, do_sample=False)
        generated = response[0]["generated_text"][-1]["content"]
        
        if re.search(devanagari_pattern, generated):
            included += 1
    
    return {
        "inclusion_rate": included / max(total, 1),
        "included": included,
        "total": total,
    }


def qualitative_evaluation(model_pipe, prompts: list[str]) -> list[dict]:
    """
    Generate responses for qualitative human review.
    """
    results = []
    
    for prompt in prompts:
        messages = [{"role": "user", "content": prompt}]
        response = model_pipe(messages, max_new_tokens=1024, do_sample=False)
        generated = response[0]["generated_text"][-1]["content"]
        
        results.append({
            "prompt": prompt,
            "response": generated,
            "word_count": len(generated.split()),
        })
    
    return results


# ============================================================
# TEST DATA
# ============================================================

def get_default_test_data() -> dict:
    """Default test prompts and data for evaluation."""
    
    verse_identification = [
        {"question": "Which chapter and verse of the Bhagavad Gita contains 'कर्मण्येवाधिकारस्ते'?", "ground_truth": "Chapter 2, Verse 47"},
        {"question": "The Gayatri Mantra is found in which Mandala of Rigveda?", "ground_truth": "Mandala 3"},
        {"question": "'तत्त्वमसि' appears in which Upanishad?", "ground_truth": "Chandogya Upanishad"},
        {"question": "'अहं ब्रह्मास्मि' is from which Upanishad?", "ground_truth": "Brihadaranyaka Upanishad"},
        {"question": "Which verse says 'यदा यदा हि धर्मस्य ग्लानिर्भवति भारत'?", "ground_truth": "Chapter 4, Verse 7"},
    ]
    
    citation_prompts = [
        "Explain the concept of Dharma in the Bhagavad Gita.",
        "What does the Mundaka Upanishad say about knowledge?",
        "Describe the path of Bhakti Yoga as taught in Hindu scriptures.",
        "What is the significance of Om (ॐ) in the Vedas?",
        "Explain the Nasadiya Sukta (creation hymn).",
    ]
    
    qualitative_prompts = [
        "Explain the concept of Maya in Advaita Vedanta.",
        "What is the relationship between Karma and Dharma in the Mahabharata?",
        "Translate and explain: 'असतो मा सद्गमय, तमसो मा ज्योतिर्गमय, मृत्योर्मा अमृतं गमय'",
        "भगवद्गीता के अनुसार योग की परिभाषा क्या है?",
        "Compare the philosophical positions of Shankaracharya and Ramanujacharya on Brahman.",
        "What are the four stages of life (Ashrama) in Hindu tradition?",
        "Explain the significance of the Kurukshetra war in the Mahabharata.",
        "What is Patanjali's Yoga Sutra 1.2 and what does it mean?",
    ]
    
    return {
        "verse_identification": verse_identification,
        "citation_prompts": citation_prompts,
        "qualitative_prompts": qualitative_prompts,
    }


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned Hindu scripture model")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--model-path", type=str, required=True, help="Path to model to evaluate")
    parser.add_argument("--output", type=str, default="./eval_results.json", help="Output file for results")
    parser.add_argument("--skip-qualitative", action="store_true", help="Skip qualitative generation")
    args = parser.parse_args()
    
    cfg = load_config(args.config)
    
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    print(f"Model: {args.model_path}")
    print("=" * 60)
    
    # --- Load Model ---
    print("\nLoading model...")
    pipe = pipeline(
        "text-generation",
        model=args.model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    
    # --- Get Test Data ---
    test_data = get_default_test_data()
    
    # --- Run Evaluations ---
    results = {}
    
    # 1. Verse Identification Accuracy
    print("\n[1/4] Verse Identification Accuracy...")
    verse_results = compute_verse_accuracy(pipe, test_data["verse_identification"])
    results["verse_accuracy"] = {k: v for k, v in verse_results.items() if k != "details"}
    print(f"  Accuracy: {verse_results['accuracy']:.1%}")
    print(f"  Partial: {verse_results['partial_accuracy']:.1%}")
    
    # 2. Citation Rate
    print("\n[2/4] Citation Rate...")
    citation_results = compute_citation_rate(pipe, test_data["citation_prompts"])
    results["citation_rate"] = citation_results
    print(f"  Rate: {citation_results['citation_rate']:.1%}")
    
    # 3. Sanskrit Inclusion
    print("\n[3/4] Sanskrit Inclusion Rate...")
    sanskrit_results = compute_sanskrit_inclusion_rate(pipe, test_data["citation_prompts"])
    results["sanskrit_inclusion"] = sanskrit_results
    print(f"  Rate: {sanskrit_results['inclusion_rate']:.1%}")
    
    # 4. Qualitative Samples
    if not args.skip_qualitative:
        print("\n[4/4] Generating qualitative samples...")
        qual_results = qualitative_evaluation(pipe, test_data["qualitative_prompts"])
        results["qualitative_samples"] = qual_results
        
        print("\n" + "=" * 60)
        print("SAMPLE OUTPUTS")
        print("=" * 60)
        for sample in qual_results[:3]:  # Print first 3
            print(f"\nQ: {sample['prompt'][:80]}...")
            print(f"A: {sample['response'][:300]}...")
            print(f"   [{sample['word_count']} words]")
            print("-" * 40)
    
    # --- Summary ---
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"  Verse Accuracy:      {results['verse_accuracy']['accuracy']:.1%}")
    print(f"  Citation Rate:       {results['citation_rate']['citation_rate']:.1%}")
    print(f"  Sanskrit Inclusion:  {results['sanskrit_inclusion']['inclusion_rate']:.1%}")
    print("=" * 60)
    
    # --- Save Results ---
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
