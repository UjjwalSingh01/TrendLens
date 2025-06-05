import os
import logging
import torch
import io
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global model and processor instances
model = None
processor = None
LABELS = []

def load_models():
    """Load CLIP model and clothing labels"""
    global model, processor, LABELS
    
    if model is None or processor is None:
        logger.info("Initializing CLIP model...")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        logger.info("CLIP model loaded")
    
    if not LABELS:
        logger.info("Loading clothing labels...")
        label_path = os.path.join(os.path.dirname(__file__), "..", "clip_labels.txt")
        
        if not os.path.exists(label_path):
            logger.error(f"Label file not found: {label_path}")
            raise FileNotFoundError(f"CLIP labels file missing at {label_path}")
        
        with open(label_path, "r") as f:
            raw_labels = [line.strip() for line in f.readlines() if line.strip()]
        
        # Prioritize Indian fashion terms
        indian_terms = {"saree", "lehenga", "salwar", "kurta", "sherwani", "dhoti", "churidar"}
        prioritized = [l for l in raw_labels if any(term in l for term in indian_terms)]
        general = [l for l in raw_labels if l not in prioritized]
        
        LABELS.extend(prioritized + general)
        logger.info(f"Loaded {len(LABELS)} clothing labels (Indian terms: {len(prioritized)})")

def process_text_batch(text_batch):
    """Process a batch of text labels"""
    return model.get_text_features(**processor(
        text=text_batch,
        return_tensors="pt",
        padding=True,
        truncation=True
    ))

def get_best_clip_label(image_bytes):
    """Classify clothing item using CLIP and DeepFashion labels"""
    try:
        load_models()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Process image
        image_inputs = processor(images=image, return_tensors="pt")
        image_features = model.get_image_features(**image_inputs)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        # Process text in parallel batches
        BATCH_SIZE = 64
        best_score = -1
        best_label = "clothing"
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, len(LABELS), BATCH_SIZE):
                batch = LABELS[i:i+BATCH_SIZE]
                futures.append(executor.submit(process_text_batch, batch))
            
            for future_idx, future in enumerate(futures):
                text_features = future.result()
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                
                # Calculate similarity
                similarity = (image_features @ text_features.T)[0]
                batch_best_idx = similarity.argmax().item()
                batch_score = similarity[batch_best_idx].item()
                
                if batch_score > best_score:
                    best_score = batch_score
                    global_idx = future_idx * BATCH_SIZE + batch_best_idx
                    best_label = LABELS[global_idx]
        
        logger.info(f"Classified as: {best_label} (confidence: {best_score:.2f})")
        return best_label
        
    except Exception as e:
        logger.error(f"CLIP classification failed: {str(e)}")
        return "clothing"