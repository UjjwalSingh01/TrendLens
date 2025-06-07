const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const callPythonService = require("../services/callPythonService");

const router = express.Router();

// Ensure uploads directory exists
const uploadDir = path.join(__dirname, "../../public/uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${Math.round(Math.random() * 1e9)}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const upload = multer({ storage, limits: { fileSize: 5 * 1024 * 1024 } });

router.post("/image", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const result = await callPythonService(req.file.path);
    const url = `/uploads/${req.file.filename}`;

    res.json({
      url,
      caption: result.caption,
      keywords: result.keywords,
      clip_label: result.clip_label
    });
    
  } catch (err) {
    // Cleanup on error
    if (req.file?.path) fs.unlinkSync(req.file.path);
    
    res.status(500).json({ 
      error: "Image processing failed",
      detail: err.message 
    });
  }
});

module.exports = router;