import os
import re
import logging
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global models
kw_model = None
sentence_model = None
FASHION_TERMS = []

def load_fashion_terms():
    """Load fashion terms from DeepFashion data"""
    global FASHION_TERMS
    
    if not FASHION_TERMS:
        logger.info("Loading fashion terminology...")
        deepfashion_dir = os.path.join(os.path.dirname(__file__), "..", "deepfashion")
        
        # Try to load from generated labels first
        label_path = os.path.join(os.path.dirname(__file__), "..", "clip_labels.txt")
        if os.path.exists(label_path):
            with open(label_path, "r") as f:
                FASHION_TERMS = [line.strip() for line in f.readlines() if line.strip()]
        
        # Fallback to Indian fashion terms
        if not FASHION_TERMS:
            FASHION_TERMS = [
                "saree", "lehenga", "salwar", "kameez", "kurta", 
                "sherwani", "dhoti", "churidar", "dupatta", "angavastram",
                "t-shirt", "dress", "jeans", "blouse", "jacket", "coat"
            ]
        
        # Preprocess terms
        processed_terms = set()
        for term in FASHION_TERMS:
            # Split multi-word terms
            processed_terms.update(term.split())
            # Add whole phrase
            processed_terms.add(term)
        
        FASHION_TERMS = list(processed_terms)
        logger.info(f"Loaded {len(FASHION_TERMS)} fashion terms")

def load_models():
    """Initialize KeyBERT model"""
    global kw_model, sentence_model
    
    if kw_model is None or sentence_model is None:
        logger.info("Initializing KeyBERT model...")
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        kw_model = KeyBERT(model=sentence_model)
        logger.info("KeyBERT model loaded")
    
    load_fashion_terms()

def extract_keywords(text):
    """Extract fashion-relevant keywords from text"""
    try:
        load_models()
        
        # Clean text
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Extract keywords with fashion focus
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            top_n=5,
            seed_keywords=FASHION_TERMS,
            diversity=0.5
        )
        
        # Post-process results
        results = []
        for kw, score in keywords:
            # Filter out non-fashion terms
            if any(term in kw for term in FASHION_TERMS):
                # Remove redundant terms
                if not any(kw in r and r != kw for r in results):
                    results.append(kw)
        
        # Fallback if no fashion terms found
        if not results:
            logger.warning("No fashion terms found, using fallback")
            return text.split()[:3]
        
        logger.info(f"Extracted keywords: {results}")
        return results
        
    except Exception as e:
        logger.error(f"Keyword extraction failed: {str(e)}")
        return text.split()[:3]