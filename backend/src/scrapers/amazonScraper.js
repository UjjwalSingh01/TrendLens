// src/scrapers/amazonScraper.js
const axios = require("axios");
const cheerio = require("cheerio");

async function scrapeAmazon(url) {
  try {
    const { data } = await axios.get(url, { 
      headers: {
        "User-Agent": "...",
        "Accept-Language": "en-US,en;q=0.9"
      }
    });

    const $ = cheerio.load(data);
    const items = [];

    $("div[data-component-type='s-search-result']").each((i, el) => {
      if (items.length >= 5) return false;

      const title = $(el).find("h2 a span").text().trim();
      const link = "https://www.amazon.in" + $(el).find("h2 a").attr("href");
      const image = $(el).find("img.s-image").attr("src");

      if (title && link && image) {
        items.push({ title, link: link.split('?')[0], image, source: "Amazon" });
      }
    });

    return items;
  } catch (err) {
    console.error("Amazon scraping error:", err.message);
    return [];
  }
}

module.exports = scrapeAmazon;
