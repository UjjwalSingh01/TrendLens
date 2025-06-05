from fastapi import FastAPI, File, UploadFile, HTTPException
from model.clip_matcher import get_best_clip_label
from model.blip_caption import generate_caption
from model.keyword_extractor import extract_keywords
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        caption = generate_caption(contents)
        keywords = extract_keywords(caption)
        label = get_best_clip_label(contents)
        
        return {
            "caption": caption,
            "keywords": keywords,
            "clip_label": label
        }
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Image processing failed")