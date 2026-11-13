"""
============================================================
DATA PROCESSING PIPELINE
============================================================
Processes raw Hindu scripture PDFs and text files into
structured datasets for SFT, DPO, and GRPO training stages.

Supports:
- Digital PDF text extraction (PyMuPDF)
- Scanned PDF OCR (Tesseract with Hindi/Sanskrit)
- Text cleaning and Unicode normalization
- Chunking into training-ready segments
- Dataset formatting for each training stage
============================================================
"""

import json
import re
import unicodedata
from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
from tqdm import tqdm


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a digital (non-scanned) PDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
    """
    doc = fitz.open(pdf_path)
    text_parts = []
    for page_num, page in enumerate(doc):
        page_text = page.get_text("text")
        if page_text.strip():
            text_parts.append(page_text)
    doc.close()
    return "\n\n".join(text_parts)


def extract_text_from_scanned_pdf(pdf_path: str, lang: str = "hin+san+eng") -> str:
    """
    Extract text from a scanned PDF using OCR.
    Requires Tesseract installed with Hindi and Sanskrit language packs.
    
    Install Tesseract:
        Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
        Linux: sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-san
        
    Args:
        pdf_path: Path to the scanned PDF
        lang: Tesseract language string (hin=Hindi, san=Sanskrit, eng=English)
        
    Returns:
        OCR-extracted text
    """
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        raise ImportError("Install pytesseract and Pillow: pip install pytesseract Pillow")
    
    doc = fitz.open(pdf_path)
    text_parts = []
    
    for page_num in tqdm(range(len(doc)), desc=f"OCR: {Path(pdf_path).name}"):
        page = doc[page_num]
        # Render page to image at 300 DPI for good OCR quality
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Run OCR
        page_text = pytesseract.image_to_string(img, lang=lang)
        if page_text.strip():
            text_parts.append(page_text)
    
    doc.close()
    return "\n\n".join(text_parts)


def detect_if_scanned(pdf_path: str, sample_pages: int = 3) -> bool:
    """
    Heuristic to detect if a PDF is scanned (image-based) vs digital.
    Checks first few pages for extractable text.
    """
    doc = fitz.open(pdf_path)
    text_chars = 0
    pages_checked = min(sample_pages, len(doc))
    
    for i in range(pages_checked):
        text_chars += len(doc[i].get_text("text").strip())
    
    doc.close()
    # If average chars per page < 50, likely scanned
    return (text_chars / max(pages_checked, 1)) < 50


# ============================================================
# TEXT CLEANING & NORMALIZATION
# ============================================================

def clean_scripture_text(text: str) -> str:
    """
    Clean extracted scripture text:
    - Normalize Unicode (NFC for Devanagari)
    - Remove page numbers, headers, footers
    - Fix common OCR errors in Devanagari
    - Remove excessive whitespace
    """
    # Unicode NFC normalization (critical for Devanagari)
    text = unicodedata.normalize("NFC", text)
    
    # Remove standalone page numbers
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)
    
    # Remove common header/footer patterns
    text = re.sub(r"^(Page|पृष्ठ)\s*\d+.*$", "", text, flags=re.MULTILINE)
    
    # Fix common OCR errors in Devanagari
    # (double matras, broken characters)
    text = re.sub(r"([ा-ौ])\1+", r"\1", text)  # Remove duplicate matras
    
    # Normalize various dash types to standard
    text = re.sub(r"[–—―]", "—", text)
    
    # Remove excessive newlines (keep max 2)
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Remove excessive spaces
    text = re.sub(r" {2,}", " ", text)
    
    # Strip each line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    
    return text.strip()


def detect_language(text: str) -> str:
    """
    Detect primary language of text chunk.
    Returns: 'sanskrit', 'hindi', 'english', or 'mixed'
    """
    devanagari_chars = len(re.findall(r"[\u0900-\u097F]", text))
    latin_chars = len(re.findall(r"[a-zA-Z]", text))
    total_chars = len(text.strip())
    
    if total_chars == 0:
        return "unknown"
    
    devanagari_ratio = devanagari_chars / total_chars
    latin_ratio = latin_chars / total_chars
    
    if devanagari_ratio > 0.5:
        # Check for Sanskrit-specific markers (vedic accents, specific words)
        sanskrit_markers = re.findall(r"(श्लोक|सूत्र|ॐ|अथ|इति|॥)", text)
        if len(sanskrit_markers) > 2:
            return "sanskrit"
        return "hindi"
    elif latin_ratio > 0.5:
        return "english"
    else:
        return "mixed"


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(text: str, max_tokens: int = 2048, overlap: int = 200) -> list[str]:
    """
    Split text into chunks suitable for training.
    Uses paragraph boundaries for natural splitting.
    
    Args:
        text: Full text to chunk
        max_tokens: Approximate max tokens per chunk (chars/4 heuristic)
        overlap: Character overlap between chunks for context continuity
        
    Returns:
        List of text chunks
    """
    # Approximate: 1 token ≈ 4 chars for English, ≈ 2 chars for Devanagari
    lang = detect_language(text)
    chars_per_token = 2 if lang in ("hindi", "sanskrit") else 4
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap * chars_per_token
    
    # Split on paragraph boundaries
    paragraphs = text.split("\n\n")
    
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_chars:
            current_chunk += para + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # Start new chunk with overlap from end of previous
            if overlap_chars > 0 and current_chunk:
                overlap_text = current_chunk[-overlap_chars:]
                current_chunk = overlap_text + "\n\n" + para + "\n\n"
            else:
                current_chunk = para + "\n\n"
    
    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


# ============================================================
# DATASET FORMATTING
# ============================================================

def format_for_continued_pretraining(chunks: list[str], output_path: str):
    """
    Format text chunks for continued pretraining (language modeling).
    Output: JSONL with {"text": "..."} format
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            if len(chunk.strip()) > 100:  # Skip very short chunks
                record = {"text": chunk}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"Wrote {len(chunks)} chunks to {output_path}")


def format_for_sft(qa_pairs: list[dict], output_path: str, system_prompt: str):
    """
    Format Q&A pairs for SFT training.
    
    Input qa_pairs format:
        [{"instruction": "...", "response": "...", "language": "..."}]
        
    Output: JSONL with conversational format
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for pair in qa_pairs:
            record = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pair["instruction"]},
                    {"role": "assistant", "content": pair["response"]},
                ]
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"Wrote {len(qa_pairs)} SFT examples to {output_path}")


def format_for_dpo(preference_pairs: list[dict], output_path: str):
    """
    Format preference pairs for DPO training.
    
    Input format:
        [{"question": "...", "chosen_response": "...", "rejected_response": "..."}]
        
    Output: JSONL with prompt/chosen/rejected format
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for pair in preference_pairs:
            record = {
                "prompt": [{"role": "user", "content": pair["question"]}],
                "chosen": [{"role": "assistant", "content": pair["chosen_response"]}],
                "rejected": [{"role": "assistant", "content": pair["rejected_response"]}],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"Wrote {len(preference_pairs)} DPO examples to {output_path}")


def format_for_grpo(verifiable_prompts: list[dict], output_path: str):
    """
    Format prompts with ground truth for GRPO training.
    
    Input format:
        [{"question": "...", "ground_truth": "...", "category": "..."}]
        
    Output: JSONL with prompt and ground_truth columns
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for item in verifiable_prompts:
            record = {
                "prompt": [{"role": "user", "content": item["question"]}],
                "ground_truth": item["ground_truth"],
            }
            if "category" in item:
                record["category"] = item["category"]
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    print(f"Wrote {len(verifiable_prompts)} GRPO examples to {output_path}")


# ============================================================
# MASTER PIPELINE
# ============================================================

def process_all_pdfs(pdf_dir: str, output_dir: str):
    """
    Process all PDFs in a directory into cleaned text chunks.
    
    Args:
        pdf_dir: Directory containing PDF files
        output_dir: Directory to save processed text
    """
    pdf_dir = Path(pdf_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(pdf_dir.glob("**/*.pdf"))
    print(f"Found {len(pdf_files)} PDF files")
    
    all_chunks = []
    
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            # Detect if scanned
            if detect_if_scanned(str(pdf_path)):
                print(f"  [OCR] {pdf_path.name}")
                raw_text = extract_text_from_scanned_pdf(str(pdf_path))
            else:
                print(f"  [Digital] {pdf_path.name}")
                raw_text = extract_text_from_pdf(str(pdf_path))
            
            # Clean
            cleaned = clean_scripture_text(raw_text)
            
            if len(cleaned) < 200:
                print(f"  [SKIP] {pdf_path.name} - too short after cleaning")
                continue
            
            # Chunk
            chunks = chunk_text(cleaned)
            all_chunks.extend(chunks)
            
            # Save individual file's extracted text
            txt_output = output_dir / f"{pdf_path.stem}.txt"
            with open(txt_output, "w", encoding="utf-8") as f:
                f.write(cleaned)
                
        except Exception as e:
            print(f"  [ERROR] {pdf_path.name}: {e}")
            continue
    
    # Save all chunks for continued pretraining
    cpt_output = output_dir / "corpus_chunks.jsonl"
    format_for_continued_pretraining(all_chunks, str(cpt_output))
    
    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to: {cpt_output}")
    return all_chunks


# ============================================================
# SYNTHETIC DATA GENERATION HELPERS
# ============================================================

def generate_sft_from_text(text_chunk: str, scripture_name: str) -> list[dict]:
    """
    Generate instruction-response pairs from a text chunk.
    This creates template-based QA pairs. For higher quality,
    use an LLM API (GPT-4/Claude) to generate diverse questions.
    
    Returns list of {"instruction": "...", "response": "..."} dicts
    """
    pairs = []
    lang = detect_language(text_chunk)
    
    # Template 1: Explain this passage
    if lang in ("sanskrit", "hindi"):
        pairs.append({
            "instruction": f"Explain the following passage from {scripture_name}:\n\n{text_chunk[:500]}",
            "response": f"This passage from {scripture_name} discusses... [To be filled by human annotator or LLM]",
            "language": lang,
        })
    
    # Template 2: Translate
    if lang == "sanskrit":
        pairs.append({
            "instruction": f"Translate this Sanskrit text from {scripture_name} into Hindi and English:\n\n{text_chunk[:300]}",
            "response": f"Translation of the Sanskrit passage from {scripture_name}:\n\nHindi: [translation]\nEnglish: [translation]",
            "language": "sanskrit",
        })
    
    # Template 3: Summary
    pairs.append({
        "instruction": f"Summarize the key teachings in this section of {scripture_name}.",
        "response": f"The key teachings from this section of {scripture_name} are... [To be filled]",
        "language": lang,
    })
    
    return pairs


def create_dpo_pair_from_sft(
    question: str, 
    good_response: str, 
    bad_response: str
) -> dict:
    """Create a single DPO preference pair."""
    return {
        "question": question,
        "chosen_response": good_response,
        "rejected_response": bad_response,
    }


# ============================================================
# SAMPLE DATA GENERATION (for testing pipeline)
# ============================================================

def generate_sample_datasets(output_dir: str):
    """
    Generate small sample datasets for testing the training pipeline.
    These are minimal examples - replace with real data for actual training.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    system_prompt = (
        "You are a knowledgeable scholar of Hindu scriptures with deep expertise "
        "in the Vedas, Upanishads, Bhagavad Gita, Ramayana, Mahabharata, and other "
        "sacred texts. You can read, translate, and explain Sanskrit, Hindi, and "
        "English texts. Always cite specific verses when possible."
    )
    
    # --- Sample SFT Data ---
    sft_data = [
        {
            "instruction": "What is the meaning of 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन' from the Bhagavad Gita?",
            "response": (
                "This verse is from Bhagavad Gita, Chapter 2, Verse 47 (कर्मण्येवाधिकारस्ते मा फलेषु कदाचन। "
                "मा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥)\n\n"
                "Translation: 'You have the right to perform your prescribed duties, but you are not entitled "
                "to the fruits of your actions. Never consider yourself to be the cause of the results of your "
                "activities, nor be attached to inaction.'\n\n"
                "This is one of the most important verses in the Gita, teaching the philosophy of Nishkama Karma "
                "(selfless action). Lord Krishna advises Arjuna that one should focus on performing one's duty "
                "without attachment to results. This doesn't mean one shouldn't desire success, but rather that "
                "the anxiety about results should not paralyze action."
            ),
            "language": "mixed",
        },
        {
            "instruction": "Explain the concept of Maya in Advaita Vedanta.",
            "response": (
                "Maya (माया) in Advaita Vedanta is one of the most profound philosophical concepts in Hindu thought.\n\n"
                "**Definition:** Maya refers to the cosmic illusion or the power that creates the appearance of "
                "multiplicity in what is actually non-dual (Advaita) Brahman. Adi Shankaracharya in his "
                "Vivekachudamani (verse 108) describes it as 'अनिर्वचनीयं' (anirvachaniyam) — that which is "
                "indescribable, neither real nor unreal.\n\n"
                "**Key aspects:**\n"
                "1. **Avarana Shakti** (आवरण शक्ति): The veiling power that hides the true nature of Brahman\n"
                "2. **Vikshepa Shakti** (विक्षेप शक्ति): The projecting power that creates the false appearance\n\n"
                "**Shankaracharya's analogy:** Just as a rope in dim light appears as a snake (rajju-sarpa nyaya), "
                "Brahman appears as the world through Maya.\n\n"
                "Maya is not 'illusion' in the sense that the world doesn't exist — it means the world doesn't "
                "exist in the way we perceive it. It has practical reality (vyavaharika satta) but not absolute "
                "reality (paramarthika satta)."
            ),
            "language": "english",
        },
        {
            "instruction": "भगवद्गीता के अनुसार कर्म योग क्या है? हिंदी में समझाएं।",
            "response": (
                "भगवद्गीता में कर्म योग का विस्तृत वर्णन मुख्यतः अध्याय 3 (कर्म योग) में मिलता है।\n\n"
                "**कर्म योग की परिभाषा:**\n"
                "कर्म योग का अर्थ है — निष्काम भाव से कर्म करना, अर्थात् फल की इच्छा के बिना अपने कर्तव्य का पालन करना।\n\n"
                "**मुख्य श्लोक:**\n"
                "श्लोक 3.9: 'यज्ञार्थात्कर्मणोऽन्यत्र लोकोऽयं कर्मबन्धनः'\n"
                "(यज्ञ के लिए किए गए कर्म के अतिरिक्त अन्य कर्म बंधन का कारण है)\n\n"
                "**कर्म योग के सिद्धांत:**\n"
                "1. कर्म करना अनिवार्य है — कोई भी क्षण बिना कर्म के नहीं रह सकता (3.5)\n"
                "2. फल में आसक्ति नहीं रखनी चाहिए (2.47)\n"
                "3. सभी कर्म ईश्वर को अर्पित करने चाहिए (3.30)\n"
                "4. समत्व बुद्धि से कर्म करना — सिद्धि-असिद्धि में समान रहना (2.48)\n\n"
                "श्रीकृष्ण कहते हैं कि कर्म त्यागने से नहीं, बल्कि कर्म में आसक्ति त्यागने से मुक्ति मिलती है।"
            ),
            "language": "hindi",
        },
        {
            "instruction": "What are the four Mahavakyas (great sayings) of the Upanishads?",
            "response": (
                "The four Mahavakyas (महावाक्य) are the foundational declarations of Advaita Vedanta, "
                "one from each of the four Vedas:\n\n"
                "1. **प्रज्ञानं ब्रह्म** (Prajnanam Brahma) — 'Consciousness is Brahman'\n"
                "   - Source: Aitareya Upanishad (Rigveda)\n"
                "   - Type: Svarupa Vakya (defines nature of Brahman)\n\n"
                "2. **अहं ब्रह्मास्मि** (Aham Brahmasmi) — 'I am Brahman'\n"
                "   - Source: Brihadaranyaka Upanishad (Yajurveda)\n"
                "   - Type: Anubhava Vakya (experiential statement)\n\n"
                "3. **तत्त्वमसि** (Tat Tvam Asi) — 'Thou art That'\n"
                "   - Source: Chandogya Upanishad (Samaveda)\n"
                "   - Type: Upadesa Vakya (teaching statement by guru)\n\n"
                "4. **अयमात्मा ब्रह्म** (Ayam Atma Brahma) — 'This Self is Brahman'\n"
                "   - Source: Mandukya Upanishad (Atharvaveda)\n"
                "   - Type: Anusandhana Vakya (contemplation statement)\n\n"
                "These four statements together establish the identity of the individual self (Atman) "
                "with the universal reality (Brahman), which is the central teaching of Advaita Vedanta."
            ),
            "language": "english",
        },
        {
            "instruction": "Translate the Gayatri Mantra and explain its significance.",
            "response": (
                "**The Gayatri Mantra:**\n\n"
                "ॐ भूर्भुवः स्वः\n"
                "तत्सवितुर्वरेण्यं\n"
                "भर्गो देवस्य धीमहि\n"
                "धियो यो नः प्रचोदयात्॥\n\n"
                "**Transliteration:** Om Bhur Bhuvah Svah, Tat Savitur Varenyam, "
                "Bhargo Devasya Dhimahi, Dhiyo Yo Nah Prachodayat\n\n"
                "**Translation:** 'We meditate upon the glorious splendor of the divine Sun (Savitri). "
                "May that divine light illuminate and inspire our intellect.'\n\n"
                "**Source:** Rigveda (Mandala 3, Sukta 62, Verse 10), attributed to Rishi Vishvamitra\n\n"
                "**Significance:**\n"
                "1. It is considered the most sacred mantra in Hinduism\n"
                "2. Traditionally recited during Sandhyavandana (morning/evening prayers)\n"
                "3. The Vyahritis (Bhur, Bhuvah, Svah) represent the three worlds: Earth, Atmosphere, Heaven\n"
                "4. Philosophically, it is a prayer for enlightenment of the buddhi (intellect)\n"
                "5. The mantra encapsulates the essence of the Vedas — the seeking of divine wisdom\n\n"
                "Shankaracharya said: 'गायत्री वेदमाता' — Gayatri is the mother of all Vedas."
            ),
            "language": "mixed",
        },
    ]
    
    # --- Sample DPO Data ---
    dpo_data = [
        {
            "question": "What does the Bhagavad Gita say about the soul?",
            "chosen_response": (
                "The Bhagavad Gita's teaching about the soul (Atman) is primarily found in Chapter 2 "
                "(Sankhya Yoga). Key verses include:\n\n"
                "**2.20:** 'न जायते म्रियते वा कदाचिन्' — The soul is never born, nor does it ever die. "
                "It is unborn, eternal, permanent, and primeval.\n\n"
                "**2.22:** 'वासांसि जीर्णानि यथा विहाय' — Just as a person discards worn-out garments and "
                "puts on new ones, the soul discards old bodies and takes on new ones.\n\n"
                "**2.23:** The soul cannot be cut by weapons, burned by fire, moistened by water, or dried by wind.\n\n"
                "These verses establish the Atman as sat-chit-ananda (existence-consciousness-bliss), "
                "which is the Vedantic understanding of the true self."
            ),
            "rejected_response": (
                "The Gita talks about souls. It says the soul is immortal and keeps being reborn. "
                "Krishna tells Arjuna not to worry because the soul can't die."
            ),
        },
        {
            "question": "Who wrote the Ramayana?",
            "chosen_response": (
                "There are two primary versions of the Ramayana:\n\n"
                "1. **Valmiki Ramayana** (वाल्मीकि रामायण): Written by Maharishi Valmiki in Sanskrit, "
                "considered the 'Adi Kavya' (first poem). It contains approximately 24,000 shlokas in 7 Kandas "
                "(books). Valmiki is called 'Adi Kavi' (the first poet).\n\n"
                "2. **Ramcharitmanas** (रामचरितमानस): Written by Goswami Tulsidas in Awadhi Hindi in the "
                "16th century CE. It consists of 7 Sopans (steps/books) and is the most popular version in "
                "North India.\n\n"
                "Other notable versions include:\n"
                "- Kamban's Ramavataram (Tamil, 12th century)\n"
                "- Krittivasi Ramayan by Krittivas Ojha (Bengali, 15th century)\n"
                "- Adhyatma Ramayana (Sanskrit, attributed to Vyasa)"
            ),
            "rejected_response": "The Ramayana was written by Valmiki. It's about Lord Rama.",
        },
        {
            "question": "हिंदू धर्म में मोक्ष क्या है?",
            "chosen_response": (
                "मोक्ष (Liberation) हिंदू धर्म के चार पुरुषार्थों में सर्वोच्च है (धर्म, अर्थ, काम, मोक्ष)।\n\n"
                "**परिभाषा:** मोक्ष का अर्थ है जन्म-मृत्यु के चक्र (संसार) से मुक्ति।\n\n"
                "**विभिन्न दर्शनों में मोक्ष:**\n\n"
                "1. **अद्वैत वेदांत** (शंकराचार्य): जीव और ब्रह्म की एकता का ज्ञान ही मोक्ष है। "
                "'ब्रह्म सत्यं जगन्मिथ्या जीवो ब्रह्मैव नापरः'\n\n"
                "2. **विशिष्टाद्वैत** (रामानुजाचार्य): भगवान विष्णु के वैकुंठ में नित्य सेवा\n\n"
                "3. **द्वैत** (मध्वाचार्य): भगवान के सामीप्य में आनंद, पर जीव और ब्रह्म सदा भिन्न\n\n"
                "4. **योग दर्शन** (पतंजलि): कैवल्य — पुरुष का प्रकृति से विवेक\n\n"
                "**मोक्ष के मार्ग** (गीता अध्याय 3, 4, 12):\n"
                "- ज्ञान योग (ज्ञान द्वारा)\n"
                "- कर्म योग (निष्काम कर्म द्वारा)\n"
                "- भक्ति योग (ईश्वर भक्ति द्वारा)"
            ),
            "rejected_response": "मोक्ष का मतलब है मुक्ति। हिंदू धर्म में इसे सबसे बड़ा लक्ष्य माना जाता है।",
        },
    ]
    
    # --- Sample GRPO Data ---
    grpo_data = [
        {
            "question": "Which chapter and verse of the Bhagavad Gita contains 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन'?",
            "ground_truth": "Chapter 2, Verse 47",
            "category": "verse_identification",
        },
        {
            "question": "Name the author of Ramcharitmanas.",
            "ground_truth": "Goswami Tulsidas",
            "category": "factual",
        },
        {
            "question": "How many chapters (Adhyayas) are in the Bhagavad Gita?",
            "ground_truth": "18",
            "category": "factual",
        },
        {
            "question": "The Gayatri Mantra appears in which Veda and Mandala?",
            "ground_truth": "Rigveda, Mandala 3",
            "category": "verse_identification",
        },
        {
            "question": "What is the Sanskrit term for the concept of 'non-violence' central to Hindu and Jain ethics?",
            "ground_truth": "Ahimsa",
            "category": "terminology",
        },
        {
            "question": "'तत्त्वमसि' (Tat Tvam Asi) is from which Upanishad?",
            "ground_truth": "Chandogya Upanishad",
            "category": "verse_identification",
        },
        {
            "question": "How many Kandas (books) are in Valmiki's Ramayana?",
            "ground_truth": "7",
            "category": "factual",
        },
        {
            "question": "Who is the guru of Arjuna in the Mahabharata for archery?",
            "ground_truth": "Dronacharya",
            "category": "factual",
        },
    ]
    
    # Write datasets
    format_for_sft(sft_data, str(output_dir / "sft_train.jsonl"), system_prompt)
    format_for_sft(sft_data[:2], str(output_dir / "sft_eval.jsonl"), system_prompt)
    format_for_dpo(dpo_data, str(output_dir / "dpo_train.jsonl"))
    format_for_dpo(dpo_data[:1], str(output_dir / "dpo_eval.jsonl"))
    format_for_grpo(grpo_data, str(output_dir / "grpo_train.jsonl"))
    
    print(f"\nSample datasets generated in: {output_dir}")
    print(f"  SFT train: {len(sft_data)} examples")
    print(f"  DPO train: {len(dpo_data)} examples")
    print(f"  GRPO train: {len(grpo_data)} examples")
    print("\n⚠️  These are minimal samples for testing. Replace with real data for actual training.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Hindu Scripture Data Processing Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Process PDFs
    pdf_parser = subparsers.add_parser("process-pdfs", help="Process PDFs into training corpus")
    pdf_parser.add_argument("--input-dir", required=True, help="Directory with PDF files")
    pdf_parser.add_argument("--output-dir", required=True, help="Output directory")
    
    # Generate samples
    sample_parser = subparsers.add_parser("generate-samples", help="Generate sample datasets for testing")
    sample_parser.add_argument("--output-dir", default="./data/processed", help="Output directory")
    
    args = parser.parse_args()
    
    if args.command == "process-pdfs":
        process_all_pdfs(args.input_dir, args.output_dir)
    elif args.command == "generate-samples":
        generate_sample_datasets(args.output_dir)
    else:
        parser.print_help()
