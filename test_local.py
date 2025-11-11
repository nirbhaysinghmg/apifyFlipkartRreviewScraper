#!/usr/bin/env python3
"""
Local test script for Flipkart Review Scraper
"""
from flipkart_scraper_apify import scrape_product_reviews_wrapper
import json

# Test URL - Canon Camera
url = "https://www.flipkart.com/canon-eos-r50-mirrorless-camera-body-rf-s-18-45-mm-f-4-5-6-3-stm/p/itm3bc65ea11d81b?pid=DLLGN2WBZ6JJS3JJ&lid=LSTDLLGN2WBZ6JJS3JJ5YX6SU"

print("=" * 80)
print("TESTING FLIPKART REVIEW SCRAPER LOCALLY")
print("=" * 80)
print(f"\nURL: {url}")
print(f"Max reviews: 10")
print("\nStarting scrape...")
print("-" * 80)

# Scrape reviews with limit of 10
reviews, count, success = scrape_product_reviews_wrapper(url, max_reviews=10)

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)
print(f"Success: {success}")
print(f"Total reviews scraped: {count}")

if success and reviews:
    print(f"\n✅ Successfully scraped {count} reviews!\n")

    # Display first 3 reviews
    for i, review in enumerate(reviews[:3], 1):
        print(f"\n--- Review #{i} ---")
        print(f"Author: {review.get('author', 'N/A')}")
        print(f"Rating: {review.get('rating', 'N/A')}/5")
        print(f"Title: {review.get('title', 'N/A')}")
        print(f"Date: {review.get('created_date', 'N/A')}")
        print(f"Certified Buyer: {review.get('certified_buyer', False)}")
        print(f"Location: {review.get('city', 'N/A')}, {review.get('state', 'N/A')}")
        print(f"Review: {review.get('review_text', 'N/A')[:150]}...")
        print(f"Helpful: {review.get('helpful_count', 0)} | Upvotes: {review.get('upvotes', 0)} | Downvotes: {review.get('downvotes', 0)}")

    if count > 3:
        print(f"\n... and {count - 3} more reviews")

    # Save to JSON file
    output_file = "test_reviews.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'url': url,
            'total_reviews': count,
            'success': success,
            'reviews': reviews
        }, f, indent=2, ensure_ascii=False)

    print(f"\n✅ All reviews saved to: {output_file}")

elif success and count == 0:
    print("\n⚠️  Scraping succeeded but no reviews were found.")
    print("This could mean:")
    print("  - The product has no reviews")
    print("  - Reviews are not accessible")
    print("  - The URL format is incorrect")
else:
    print("\n❌ Scraping failed!")
    print("Possible reasons:")
    print("  - Connection blocked (HTTP 403/529)")
    print("  - Cookies expired - need to update cookies in flipkart_scraper_apify.py")
    print("  - Invalid URL format")
    print("  - Network connectivity issues")
    print("\nTry:")
    print("  1. Check if the URL works in your browser")
    print("  2. Update cookies in flipkart_scraper_apify.py")
    print("  3. Use a proxy if being blocked")

print("\n" + "=" * 80)
