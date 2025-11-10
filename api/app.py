from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, HttpUrl

from flipkart_scraper_apify import (
    extract_product_id_from_url,
    scrape_product_reviews_wrapper
)

from typing import List, Dict, Any

import uvicorn

app = FastAPI(title="Flipkart Review Scraper API")

class ReviewResponse(BaseModel):
    flipkart_url: HttpUrl
    total_reviews: int
    success: bool
    reviews: List[Dict[str, Any]]

@app.get("/scrape", response_model=ReviewResponse)
def scrape_reviews(
    flipkart_url: HttpUrl = Query(..., description="Flipkart URL to scrape the reviews"),
    max_reviews: int = Query(None, description="Maximum number of reviews to scrape. If not specified, scrapes all reviews.", ge=1)
):
    """
    Scrape reviews from a Flipkart product URL.

    Args:
        flipkart_url: Flipkart product URL (must contain /p/)
        max_reviews: Optional maximum number of reviews to scrape (must be >= 1). If None, scrapes all reviews.

    Returns:
        ReviewResponse with list of reviews and metadata
    """
    try:
        # Validate URL format
        review_url, _, _ = extract_product_id_from_url(str(flipkart_url))

        if not review_url:
            raise HTTPException(
                status_code=400,
                detail="Invalid Flipkart Product URL (missing /p/)"
            )

        # Scrape reviews
        reviews, review_count, success = scrape_product_reviews_wrapper(
            str(flipkart_url),
            max_reviews=max_reviews
        )

        return ReviewResponse(
            flipkart_url=flipkart_url,
            total_reviews=review_count,
            success=success,
            reviews=reviews
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scraping reviews: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)