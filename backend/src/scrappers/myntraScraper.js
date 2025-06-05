const axios = require("axios");
const cheerio = require("cheerio");

module.exports = async function scrapeMyntra(url) {
  try {
    const { data } = await axios.get(url, { 
      headers: { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
      } 
    });
    
    const $ = cheerio.load(data);
    const items = [];
    
    $("li.product-base", data).each((i, el) => {
      if(items.length >= 5) return false;
      
      const title = $(el).find("h4.product-product").text();
      const link = "https://www.myntra.com/" + $(el).find("a.product-base-link").attr("href");
      const image = $(el).find("img.img-responsive").attr("src");
      
      if(title && link && image) {
        items.push({ 
          title, 
          link, 
          image,
          source: "Myntra"
        });
      }
    });
    
    return items;
  } catch (err) {
    console.error("Myntra scraping error:", err.message);
    return [];
  }
};