from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import logging

logger = logging.getLogger(__name__)
processor = None
model = None

def load_models():
    global processor, model
    if processor is None or model is None:
        logger.info("Loading BLIP base model...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        logger.info("BLIP base model loaded")

def generate_caption(image: Image.Image) -> str:
    load_models()
    try:
        inputs = processor(images=image, return_tensors="pt")
        output = model.generate(**inputs, max_length=50)
        return processor.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        logger.error(f"BLIP captioning failed: {e}")
        return "fashion item"
