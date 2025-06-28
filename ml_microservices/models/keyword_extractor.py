import os
import re
import logging
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

kw_model = None
sentence_model = None
FASHION_TERMS = []

def load_fashion_terms():
    global FASHION_TERMS
    if not FASHION_TERMS:
        label_path = os.path.join(os.path.dirname(__file__), "..", "clip_labels.txt")
        if os.path.exists(label_path):
            with open(label_path, "r") as f:
                terms = [line.strip() for line in f if line.strip()]
        else:
            terms = [
                "saree", "lehenga", "kurta", "salwar", "gown", "dress", "t-shirt",
                "shirt", "jacket", "jeans", "blazer", "skirt", "crop top", "coat",
                "floral", "sleeveless", "bodycon", "maxi dress", "mini skirt",
                "hoodie", "kurti", "palazzo", "co-ord", "jumpsuit"
            ]

        processed_terms = set()
        for term in terms:
            processed_terms.update(term.split())
            processed_terms.add(term)
        
        FASHION_TERMS = list(processed_terms)
        logger.info(f"Loaded {len(FASHION_TERMS)} fashion terms")

def load_models():
    global kw_model, sentence_model
    if kw_model is None or sentence_model is None:
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        kw_model = KeyBERT(model=sentence_model)
        logger.info("KeyBERT and sentence-transformer loaded")
    load_fashion_terms()

def extract_keywords(caption: str, clip_label: str = ""):
    try:
        load_models()

        combined_text = f"{caption} {clip_label}".lower().strip()
        combined_text = re.sub(r'[^\w\s]', '', combined_text)

        keywords = kw_model.extract_keywords(
            combined_text,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            top_n=10,
            seed_keywords=FASHION_TERMS,
            diversity=0.3
        )

        result = []
        for kw, score in keywords:
            if any(term in kw for term in FASHION_TERMS):
                if kw not in result and not any(kw in r and r != kw for r in result):
                    result.append(kw)

        if not result:
            logger.warning("No fashion keywords found, using fallback")
            return combined_text.split()[:3]

        logger.info(f"Extracted keywords: {result}")
        return result[:5]

    except Exception as e:
        logger.exception("Keyword extraction failed")
        return caption.split()[:3]
