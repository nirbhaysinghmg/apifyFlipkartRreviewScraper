# Flipkart Review Scraper API - Deployment Guide

## Quick Start

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the application**:
```bash
python api/app.py
```

3. **Access the API**:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

## Docker Deployment

### Option 1: Using Docker Compose (Recommended)

1. **Build and run**:
```bash
docker-compose up -d
```

2. **View logs**:
```bash
docker-compose logs -f
```

3. **Stop the service**:
```bash
docker-compose down
```

### Option 2: Using Docker directly

1. **Build the image**:
```bash
docker build -t flipkart-scraper-api .
```

2. **Run the container**:
```bash
docker run -d \
  --name flipkart-scraper-api \
  -p 8000:8000 \
  flipkart-scraper-api
```

3. **View logs**:
```bash
docker logs -f flipkart-scraper-api
```

4. **Stop the container**:
```bash
docker stop flipkart-scraper-api
docker rm flipkart-scraper-api
```

---

## API Usage

### Scrape All Reviews
```bash
curl "http://localhost:8000/scrape?flipkart_url=https://www.flipkart.com/product/p/item123"
```

### Scrape Limited Reviews (e.g., 50 reviews)
```bash
curl "http://localhost:8000/scrape?flipkart_url=https://www.flipkart.com/product/p/item123&max_reviews=50"
```

### Using Python
```python
import requests

url = "http://localhost:8000/scrape"
params = {
    "flipkart_url": "https://www.flipkart.com/product/p/item123",
    "max_reviews": 100  # Optional
}

response = requests.get(url, params=params)
data = response.json()

print(f"Total reviews: {data['total_reviews']}")
print(f"Success: {data['success']}")
for review in data['reviews']:
    print(f"- {review['title']}: {review['rating']}/5")
```

---

## Environment Variables

Create a `.env` file for configuration:

```bash
# Proxy Configuration (Optional)
PROXY_HTTP_URL=http://username:password@proxy:port
PROXY_HTTPS_URL=https://username:password@proxy:port
```

---

## Production Deployment

### Using Uvicorn with Workers

For production, use multiple workers:

```bash
uvicorn api.app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

### Using Gunicorn (Recommended for Production)

```bash
gunicorn api.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info
```

### Docker with Custom Port

```bash
docker run -d \
  --name flipkart-scraper-api \
  -p 8080:8000 \
  -e PROXY_HTTP_URL=http://proxy:port \
  flipkart-scraper-api
```

---

## Health Check

Check if the API is running:

```bash
curl http://localhost:8000/docs
```

---

## Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)
```

### Docker build fails
```bash
# Clean up Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t flipkart-scraper-api .
```

### Container crashes immediately
```bash
# Check logs
docker logs flipkart-scraper-api

# Run interactively for debugging
docker run -it --rm flipkart-scraper-api /bin/bash
```

---

## Cloud Deployment

### Deploy to Google Cloud Run
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/flipkart-scraper-api

# Deploy
gcloud run deploy flipkart-scraper-api \
  --image gcr.io/PROJECT_ID/flipkart-scraper-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy to AWS ECS/Fargate
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker tag flipkart-scraper-api:latest ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/flipkart-scraper-api:latest

docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/flipkart-scraper-api:latest
```

### Deploy to Heroku
```bash
# Login to Heroku
heroku login
heroku container:login

# Push and release
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

---

## Performance Tips

1. **Use max_reviews parameter** to limit scraping time for faster responses
2. **Implement caching** for frequently accessed products
3. **Use a reverse proxy** (Nginx) for load balancing
4. **Monitor rate limits** to avoid being blocked by Flipkart
5. **Use proxies** if scraping at scale

---

## Security

1. **Don't expose sensitive data** in environment variables
2. **Use HTTPS** in production with SSL certificates
3. **Implement rate limiting** to prevent abuse
4. **Use authentication** for production APIs
5. **Keep dependencies updated** regularly

```bash
# Update dependencies
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```
