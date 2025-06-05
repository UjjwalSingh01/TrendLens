from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

# Load model once
kw_model = None
sentence_model = None

def load_models():
    global kw_model, sentence_model
    if kw_model is None or sentence_model is None:
        logger.info("Loading KeyBERT model...")
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        kw_model = KeyBERT(model=sentence_model)

def extract_keywords(text):
    load_models()
    try:
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=3
        )
        return [kw[0] for kw in keywords]
    except Exception as e:
        logger.error(f"Keyword extraction failed: {str(e)}")
        return text.split()[:3]  # Fallback to first 3 words