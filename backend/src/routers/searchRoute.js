const express = require("express");
const path = require("path");
const { buildSearchUrls } = require("../services/buildSearchUrls");
const scrapeAmazon = require("../scrapers/amazonScraper");
const scrapeFlipkart = require("../scrapers/flipkartScraper");
const scrapeMyntra = require("../scrapers/myntraScraper");

const router = express.Router();

router.post("/products", async (req, res) => {
  try {
    const { caption, keywords, clip_label } = req.body; // MODIFIED
    
    // Combine all metadata for better search results
    const searchTerms = [clip_label, ...keywords, ...caption.split(" ")]; 
    
    const urls = buildSearchUrls(searchTerms); // MODIFIED
    
    const results = await Promise.allSettled([
      scrapeAmazon(urls.amazon),
      scrapeFlipkart(urls.flipkart),
      scrapeMyntra(urls.myntra)
    ]);
    
    const successfulResults = results
      .filter(r => r.status === "fulfilled")
      .flatMap(r => r.value);
      
    res.json({ results: successfulResults });
  } catch (err) {
    res.status(500).json({ error: "Search failed", detail: err.message });
  }
});

module.exports = router;