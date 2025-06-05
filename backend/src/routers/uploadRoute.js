const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const callPythonService = require("../services/callPythonService");

const router = express.Router();
const upload = multer({ dest: "uploads/" });

router.post("/image", upload.single("image"), async (req, res) => {
  try {
    const filePath = path.resolve(req.file.path);
    const result = await callPythonService(filePath);
    fs.unlinkSync(filePath);
    res.json(result);
  } catch (err) {
    res.status(500).json({ 
      error: "Image processing failed",
      detail: err.message 
    });
  }
});

module.exports = router;