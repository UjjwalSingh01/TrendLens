import os
import logging
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
model = None
processor = None
LABELS = []

def load_models():
    global model, processor, LABELS
    if model is None or processor is None:
        logger.info("Loading CLIP model...")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        logger.info("CLIP model loaded")

    if not LABELS:
        label_path = os.path.join(os.path.dirname(__file__), "clip_labels.txt")
        if not os.path.exists(label_path):
            raise FileNotFoundError(f"Missing clip_labels.txt at {label_path}")
        with open(label_path, "r") as f:
            LABELS.extend([line.strip() for line in f if line.strip()])
        logger.info(f"Loaded {len(LABELS)} labels")

def process_text_batch(texts):
    return model.get_text_features(**processor(text=texts, return_tensors="pt", padding=True, truncation=True))

def get_best_clip_label(image: Image.Image) -> str:
    try:
        load_models()
        image_inputs = processor(images=image, return_tensors="pt")
        image_features = model.get_image_features(**image_inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)

        best_score = -1
        best_label = "clothing"
        BATCH_SIZE = 64

        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, len(LABELS), BATCH_SIZE):
                futures.append(executor.submit(process_text_batch, LABELS[i:i+BATCH_SIZE]))

            for batch_idx, future in enumerate(futures):
                text_features = future.result()
                text_features /= text_features.norm(dim=-1, keepdim=True)
                similarity = (image_features @ text_features.T)[0]
                best_idx = similarity.argmax().item()
                score = similarity[best_idx].item()
                if score > best_score:
                    best_score = score
                    best_label = LABELS[batch_idx * BATCH_SIZE + best_idx]

        return best_label
    except Exception as e:
        logger.error(f"CLIP label extraction failed: {e}")
        return "clothing"
