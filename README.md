# Flipkart Review Scraper API

**Extract authentic product reviews from Flipkart**

A FastAPI-based REST API that scrapes and returns actual reviews from Flipkart product pages with comprehensive details including ratings, review text, author information, location, images, votes, and metadata.

## ⚠️ Important Notice

**Flipkart's displayed review counts are often inflated and don't reflect actual reviews available.** The review count shown on their website is typically fake or manipulated for marketing purposes. This API returns only the genuine, scrapeable reviews that actually exist on the platform. Don't be surprised if the actual review count differs significantly from what Flipkart displays.

## Features

- 🚀 Fast and efficient scraping with automatic pagination
- 📊 Comprehensive review data extraction
- 🎯 Configurable review limits (scrape all or limit to N reviews)
- 🔄 Automatic retry logic with error handling
- 🐳 Docker-ready for easy deployment
- 📚 Interactive API documentation (Swagger UI)
- ✅ Health checks and monitoring

## Quick Start

### Using Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access API at http://localhost:8000/docs
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python api/app.py

# Access API at http://localhost:8000/docs
```

## API Usage

### Endpoint

```
GET /scrape
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `flipkart_url` | string (URL) | Yes | Flipkart product URL (must contain `/p/`) |
| `max_reviews` | integer | No | Maximum number of reviews to scrape. If not specified, scrapes all available reviews. Must be >= 1 |

### Example Requests

**Scrape all reviews:**
```bash
curl "http://localhost:8000/scrape?flipkart_url=https://www.flipkart.com/product/p/item123"
```

**Scrape limited reviews (e.g., 50):**
```bash
curl "http://localhost:8000/scrape?flipkart_url=https://www.flipkart.com/product/p/item123&max_reviews=50"
```

**Using Python:**
```python
import requests

url = "http://localhost:8000/scrape"
params = {
    "flipkart_url": "https://www.flipkart.com/product/p/item123",
    "max_reviews": 100  # Optional
}

response = requests.get(url, params=params)
data = response.json()

print(f"Total reviews scraped: {data['total_reviews']}")
print(f"Success: {data['success']}")

for review in data['reviews']:
    print(f"{review['rating']}⭐ - {review['title']}")
    print(f"By {review['author']} from {review['city']}")
    print(f"{review['review_text']}\n")
```

### Response Format

```json
{
  "flipkart_url": "https://www.flipkart.com/product/p/item123",
  "total_reviews": 150,
  "success": true,
  "reviews": [
    {
      "review_id": "REV123",
      "author": "John Doe",
      "certified_buyer": true,
      "verified_purchase": true,
      "created_date": "2024-01-15",
      "rating": 5,
      "title": "Excellent product!",
      "review_text": "Great quality and value for money...",
      "helpful_count": 42,
      "upvotes": 40,
      "downvotes": 2,
      "city": "Mumbai",
      "state": "Maharashtra",
      "image_count": 2,
      "image_urls": "https://..., https://...",
      "position": "1",
      "review_language": "en"
    }
  ]
}
```

## Review Data Fields

Each review includes:

- **Basic Info**: `review_id`, `author`, `title`, `review_text`, `rating`, `created_date`
- **Verification**: `certified_buyer`, `verified_purchase`
- **Engagement**: `helpful_count`, `upvotes`, `downvotes`
- **Location**: `city`, `state`
- **Media**: `image_count`, `image_urls` (comma-separated)
- **Metadata**: `position`, `review_language`
- **Product Attributes**: Dynamic fields based on product (e.g., `product_color`, `product_size`)

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Docker deployment
- Docker Compose setup
- Cloud deployment (GCP, AWS, Heroku)
- Production configuration
- Troubleshooting

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Requests** - HTTP library for scraping
- **Uvicorn** - Lightning-fast ASGI server
- **Docker** - Containerization for easy deployment

## Project Structure

```
.
├── api/
│   └── app.py                 # FastAPI application
├── flipkart_scraper_apify.py  # Core scraping logic
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── .dockerignore              # Docker build exclusions
├── DEPLOYMENT.md              # Deployment guide
└── README.md                  # This file
```

## Why Review Counts Don't Match

Flipkart often displays inflated review counts on their product pages for several reasons:

1. **Marketing Strategy**: Higher review counts create social proof and trust
2. **Deleted Reviews**: Some reviews get removed but counts aren't updated
3. **Filtered Reviews**: Not all reviews are publicly accessible
4. **Manipulated Metrics**: Counts may include internal/test reviews
5. **Regional Differences**: Some reviews may be region-specific

**This API scrapes only the actual, publicly available reviews** that can be accessed through pagination, giving you the real picture.

## Performance Tips

- Use `max_reviews` parameter to limit scraping time for faster responses
- Consider implementing caching for frequently accessed products
- Use proxies if scraping at scale to avoid rate limiting
- Monitor API health using the `/docs` endpoint

## License

MIT License - feel free to use this for your projects!

## Disclaimer

This tool is for educational and research purposes only. Please respect Flipkart's terms of service and use responsibly. The scraper should not be used for commercial purposes without proper authorization.

## Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Made with ❤️ for transparent e-commerce data**
