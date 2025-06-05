from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch, io
import logging

logger = logging.getLogger(__name__)

# Load model and labels once
model = None
processor = None
LABELS = []

def load_models():
    global model, processor, LABELS
    if model is None or processor is None or not LABELS:
        logger.info("Loading CLIP model...")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Load clothing labels
        with open("clip_labels.txt") as f:
            LABELS.extend([line.strip() for line in f.readlines()])
        logger.info(f"Loaded {len(LABELS)} clothing labels")

def get_best_clip_label(image_bytes):
    load_models()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        inputs = processor(
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        # Get image features
        image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        # Get text features
        text_inputs = processor(
            text=LABELS,
            return_tensors="pt",
            padding=True,
            truncation=True
        )
        text_features = model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        # Calculate similarity
        similarity = (image_features @ text_features.T) * 100
        best_idx = similarity.argmax().item()
        
        return LABELS[best_idx]
    
    except Exception as e:
        logger.error(f"CLIP classification failed: {str(e)}")
        return "clothing"