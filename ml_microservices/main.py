from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.clip_matcher import get_best_clip_label
from models.blip_caption import generate_caption
from models.keyword_extractor import extract_keywords
from deepfashion.generate_labels import generate_labels
from PIL import Image
import io
import logging

logger = logging.getLogger("uvicorn")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        logger.error(f"Image read failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid image")

    try:
        caption = generate_caption(image)
        label = get_best_clip_label(image)
        keywords = extract_keywords(f"{caption} {label}")
        return {"caption": caption, "keywords": keywords, "clip_label": label}
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")

@app.get("/generate-labels")
async def generate_labels_endpoint():
    try:
        generate_labels()
        return {"status": "success", "message": "Labels generated"}
    except Exception as e:
        logger.error(f"Label generation failed: {e}")
        raise HTTPException(status_code=500, detail="Label generation failed")
