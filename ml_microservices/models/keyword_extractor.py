import os
import re
import logging
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)
kw_model = None
sentence_model = None
FASHION_TERMS = []

def load_fashion_terms():
    global FASHION_TERMS
    if FASHION_TERMS:
        return
    label_path = os.path.join(os.path.dirname(__file__), "clip_labels.txt")
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            FASHION_TERMS.extend([line.strip().lower() for line in f if line.strip()])
    else:
        FASHION_TERMS.extend([
            "saree", "lehenga", "kurta", "salwar", "gown", "dress",
            "jacket", "blouse", "tunic", "skirt", "crop top", "jeans"
        ])
    FASHION_TERMS = list(set(FASHION_TERMS))

def load_models():
    global kw_model, sentence_model
    if not kw_model or not sentence_model:
        logger.info("Loading KeyBERT...")
        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        kw_model = KeyBERT(model=sentence_model)
    load_fashion_terms()

def extract_keywords(text: str):
    try:
        load_models()
        text = re.sub(r"[^\w\s]", "", text.lower())
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words="english", top_n=10)
        result = [kw for kw, _ in keywords if any(term in kw for term in FASHION_TERMS)]
        return list(dict.fromkeys(result))[:5] or text.split()[:3]
    except Exception as e:
        logger.error(f"Keyword extraction failed: {e}")
        return text.split()[:3]
