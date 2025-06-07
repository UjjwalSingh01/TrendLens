const express = require("express");
const { generateLabels } = require("../services/labelGenerator");
const router = express.Router();

router.get("/generate", async (req, res) => {
  try {
    await generateLabels();
    res.json({ success: true, message: "Labels generated successfully" });
  } catch (err) {
    res.status(500).json({ 
      error: "Label generation failed",
      detail: err.message 
    });
  }
});

module.exports = router;