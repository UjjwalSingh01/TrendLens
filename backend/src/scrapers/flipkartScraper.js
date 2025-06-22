const axios = require("axios");
const cheerio = require("cheerio");

async function scrapeFlipkart(url) {
  try {
    const { data } = await axios.get(url, { 
      headers: { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
      } 
    });
    
    const $ = cheerio.load(data);
    const items = [];
    
    $("div[data-id]", data).each((i, el) => {
      if(items.length >= 5) return false;
      
      const title = $(el).find("a.IRpwTa").text() || $(el).find("a.s1Q9rs").text();
      const link = "https://www.flipkart.com" + ($(el).find("a.IRpwTa").attr("href") || $(el).find("a.s1Q9rs").attr("href"));
      const image = $(el).find("img._396cs4").attr("src");
      
      if(title && link && image) {
        items.push({ 
          title, 
          link, 
          image,
          source: "Flipkart"
        });
      }
    });
    
    return items;
  } catch (err) {
    console.error("Flipkart scraping error:", err.message);
    return [];
  }
};

module.exports = scrapeFlipkart;