# Sitemap Examples

This directory contains examples demonstrating how to use the `sitemap` endpoint to extract URLs from website sitemaps.

## 📁 Examples

### 1. Basic Sitemap Extraction (`sitemap_example.js`)

Demonstrates the basic usage of the sitemap endpoint:
- Extract all URLs from a website's sitemap
- Display the URLs
- Save URLs to a text file
- Save complete response as JSON

**Usage:**
```bash
node sitemap_example.js
```

**What it does:**
1. Calls the sitemap API with a target website URL
2. Retrieves all URLs from the sitemap
3. Displays the first 10 URLs in the console
4. Saves all URLs to `sitemap_urls.txt`
5. Saves the full response to `sitemap_urls.json`

### 2. Advanced: Sitemap + SmartScraper (`sitemap_with_smartscraper.js`)

Shows how to combine sitemap extraction with smartScraper for batch processing:
- Extract sitemap URLs
- Filter URLs based on patterns (e.g., blog posts)
- Scrape selected URLs with smartScraper
- Display results and summary

**Usage:**
```bash
node sitemap_with_smartscraper.js
```

**What it does:**
1. Extracts all URLs from a website's sitemap
2. Filters URLs (example: only blog posts or specific sections)
3. Scrapes each filtered URL using smartScraper
4. Extracts structured data from each page
5. Displays a summary of successful and failed scrapes

**Use Cases:**
- Bulk content extraction from blogs
- E-commerce product catalog scraping
- News article aggregation
- Content migration and archival

## 🔑 Setup

Before running the examples, make sure you have:

1. **API Key**: Set your ScrapeGraph AI API key as an environment variable:
   ```bash
   export SGAI_APIKEY="your-api-key-here"
   ```

   Or create a `.env` file in the project root:
   ```
   SGAI_APIKEY=your-api-key-here
   ```

2. **Dependencies**: Install required packages:
   ```bash
   npm install
   ```

## 📊 Expected Output

### Basic Sitemap Example Output:
```
🗺️  Extracting sitemap from: https://example.com/
⏳ Please wait...

✅ Sitemap extracted successfully!
📊 Total URLs found: 150

📄 First 10 URLs:
   1. https://example.com/
   2. https://example.com/about
   3. https://example.com/products
   ...

💾 URLs saved to: sitemap_urls.txt
💾 JSON saved to: sitemap_urls.json
```

### Advanced Example Output:
```
🗺️  Step 1: Extracting sitemap from: https://example.com/
⏳ Please wait...

✅ Sitemap extracted successfully!
📊 Total URLs found: 150

🎯 Selected 3 URLs to scrape:
   1. https://example.com/blog/post-1
   2. https://example.com/blog/post-2
   3. https://example.com/blog/post-3

🤖 Step 2: Scraping selected URLs...

📄 Scraping (1/3): https://example.com/blog/post-1
   ✅ Success
...

📈 Summary:
   ✅ Successful: 3
   ❌ Failed: 0
   📊 Total: 3
```

## 💡 Tips

1. **Rate Limiting**: When scraping multiple URLs, add delays between requests to avoid rate limiting
2. **Error Handling**: Always use try/catch blocks to handle API errors gracefully
3. **Filtering**: Use URL patterns to filter specific sections (e.g., `/blog/`, `/products/`)
4. **Batch Size**: Start with a small batch to test before processing hundreds of URLs

## 🔗 Related Documentation

- [Sitemap API Documentation](../../README.md#sitemap)
- [SmartScraper Documentation](../../README.md#smart-scraper)
- [ScrapeGraph AI API Docs](https://docs.scrapegraphai.com)
