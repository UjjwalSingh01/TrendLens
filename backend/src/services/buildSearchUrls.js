module.exports.buildSearchUrls = (keywords) => {
  const query = encodeURIComponent(keywords.join(" "));
  return {
    amazon: `https://www.amazon.in/s?k=${query}`,
    flipkart: `https://www.flipkart.com/search?q=${query}`,
    myntra: `https://www.myntra.com/${query}?rawQuery=${encodeURIComponent(query)}`,
  };
};