from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch, io
import logging

logger = logging.getLogger(__name__)

# Load model once at startup 
processor = None
model = None

def load_models():
    global processor, model
    if processor is None or model is None:
        logger.info("Loading BLIP model...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        logger.info("BLIP model loaded")

def generate_caption(image_bytes):
    load_models()
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs, max_length=50)
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception as e:
        logger.error(f"Caption generation failed: {str(e)}")
        return "clothing item"