from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.clip_matcher import get_best_clip_label
from models.blip_caption import generate_caption
from models.keyword_extractor import extract_keywords
from deepfashion.generate_labels import generate_labels
import logging
import numpy as np
from PIL import Image
import io
import os

app = FastAPI()
logger = logging.getLogger("uvicorn")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        # Read image content
        contents = await file.read()
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Process image
        caption = generate_caption(image)
        keywords = extract_keywords(caption)
        label = get_best_clip_label(image)
        
        return {
            "caption": caption,
            "keywords": keywords,
            "clip_label": label
        }
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image processing failed")

# NEW: Add label generation endpoint
@app.get("/generate-labels")
async def generate_labels_endpoint():
    try:
        generate_labels()
        return {"status": "success", "message": "Labels generated"}
    except Exception as e:
        logger.error(f"Label generation failed: {str(e)}")
        raise HTTPException(500, "Label generation failed")