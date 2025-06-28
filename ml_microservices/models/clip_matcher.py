import os
import logging
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

model = None
processor = None
LABELS = []

def load_models():
    global model, processor, LABELS

    if model is None or processor is None:
        logger.info("Loading CLIP model...")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        logger.info("CLIP model loaded.")

    if not LABELS:
        label_path = os.path.join(os.path.dirname(__file__), "clip_labels.txt")
        if not os.path.exists(label_path):
            raise FileNotFoundError(f"clip_labels.txt not found at {label_path}")
        
        with open(label_path, "r") as f:
            LABELS = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Loaded {len(LABELS)} CLIP labels")

def process_text_batch(text_batch):
    return model.get_text_features(**processor(
        text=text_batch,
        return_tensors="pt",
        padding=True,
        truncation=True
    ))

def get_best_clip_label(image: Image.Image) -> str:
    try:
        load_models()

        image_inputs = processor(images=image, return_tensors="pt")
        image_features = model.get_image_features(**image_inputs)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        best_score = -1
        best_label = "unknown"

        BATCH_SIZE = 64
        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(0, len(LABELS), BATCH_SIZE):
                batch = LABELS[i:i+BATCH_SIZE]
                futures.append(executor.submit(process_text_batch, batch))

            for future_idx, future in enumerate(futures):
                text_features = future.result()
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)

                similarity = (image_features @ text_features.T)[0]
                batch_best_idx = similarity.argmax().item()
                batch_score = similarity[batch_best_idx].item()

                if batch_score > best_score and batch_score > 0.25:  # ADDED THRESHOLD
                    best_score = batch_score
                    global_idx = future_idx * BATCH_SIZE + batch_best_idx
                    best_label = LABELS[global_idx]

        logger.info(f"CLIP classified as: {best_label} (confidence: {best_score:.2f})")
        return best_label

    except Exception as e:
        logger.exception("CLIP classification failed")
        return "clothing"
