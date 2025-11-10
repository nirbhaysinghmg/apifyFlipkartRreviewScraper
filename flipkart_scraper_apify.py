#!/usr/bin/env python3
"""
Flipkart Review Scraper - Fetches reviews from Flipkart product pages
"""

import requests
import json
import re
import os
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 5

# =========================
# 🔧 Oxylabs Configuration
# =========================
PROXY_CONFIG = {
    'http': os.getenv("PROXY_HTTP_URL") or os.getenv("PROXY_HTTP"),
    'https': os.getenv("PROXY_HTTPS_URL") or os.getenv("PROXY_HTTPS"),
}


# Cookies and headers from the original script (Updated: 2025-11-06)
cookies = {
    'T': 'TI175656929809300096785495785545882104171201775916513594149681348696',
    'K-ACTION': 'null',
    'rt': 'null',
    'AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg': '1',
    'ud': '3.1YH-VQLXEJIPFTR2NXRbtsjd89nJw5RivbY12vTbjUnDx2Hc_1ilz9sYRUZqtQcIOGCbhqjH3liGHwuVdM9CKLIj49EA6Y1Kyq29b3dhsNOaUfeyg3ewBmceAPM1RB2eYb165kpXmrompI0oCeZR1-uCp2EsbyUyfbhMT1bxKQvrWsACwqTImwtNpqntYyhLOGI_sk5ubgmQ1fE__2mkxQ',
    'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFkOTYzYzUwLTM0YjctNDA1OC1iMTNmLWY2NDhiODFjYTBkYSJ9.eyJleHAiOjE3NjM5NTkxMzUsImlhdCI6MTc2MjIzMTEzNSwiaXNzIjoia2V2bGFyIiwianRpIjoiMmNkYWIxMmMtNjgzZS00MzdjLThlOTAtZWNjNTY2OWZlNzk5IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNzU2NTY5Mjk4MDkzMDAwOTY3ODU0OTU3ODU1NDU4ODIxMDQxNzEyMDE3NzU5MTY1MTM1OTQxNDk2ODEzNDg2OTYiLCJrZXZJZCI6IlZJQzZCOTkxMTQ2RDE2NEM4REI4QUIwOTdCRkEwQjM5NUIiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJDSCIsIm0iOnRydWUsImdlbiI6NH0.Z1OdZaXgCfHSLkv_z0uyYrBusT6BOANxyf1Qlhvw2hQ',
    's_sq': 'flipkart-prd%3D%2526pid%253Dwww.flipkart.com%25253Alg-8-kg-5-star-smart-inverter-technology-turbodrum-diagnosis-soft-closing-door-fully-automatic-top-load-washing-machine-black%25253Aproduct-reviews%25253Aitma69f01a7f0c0a%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.flipkart.com%25252Flg-8-kg-5-star-smart-inverter-technology-turbodrum-diagnosis-soft-closing-d%2526ot%253DA',
    'vd': 'VIC6B991146D164C8DB8AB097BFA0B395B-1756569306498-36.1762453007.1762446994.159451079',
    'S': 'd1t19Pz8TRVI/ImVabj9uHj8/EMP8ix9VhnghfqKTYchw4pj9e0K2yGZLpKJTKG+E7LXpVQ/2Y2vJbyoWwqQG/NZhLw==',
    'SN': 'VIC6B991146D164C8DB8AB097BFA0B395B.TOK29D070EF2824439C8D38A92A3DDDF4A2.1762453015816.LO',
    'AMCV_17EB401053DAF4840A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C20399%7CMCMID%7C58981570769183976403714749427124473329%7CMCAID%7CNONE%7CMCOPTOUT-1762460216s%7CNONE',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-GB,en;q=0.8',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-full-version-list': '"Brave";v="141.0.0.0", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"15.5.0"',
}


def extract_json_from_html(html_content: str) -> Dict[str, Any]:
    """
    Extract the JSON data from HTML content.

    Args:
        html_content: HTML string

    Returns:
        Dictionary containing the parsed JSON data
    """
    # Find the window.__INITIAL_STATE__ JSON object
    pattern = r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});'
    match = re.search(pattern, html_content, re.DOTALL)

    if not match:
        raise ValueError("Could not find __INITIAL_STATE__ in HTML")

    json_str = match.group(1)
    return json.loads(json_str)


def extract_reviews_from_json(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract review data from the JSON structure using recursive search.

    Args:
        data: Parsed JSON data

    Returns:
        List of review dictionaries
    """
    reviews = []

    def find_reviews_recursive(obj):
        """Recursively search for ProductReviewValue objects with their component context"""
        if isinstance(obj, dict):
            # Check if this object is a renderable component with ProductReviewValue
            if 'value' in obj and isinstance(obj['value'], dict):
                if obj['value'].get('type') == 'ProductReviewValue':
                    review = extract_review_details(obj['value'], obj)
                    reviews.append(review)

            # Continue searching in nested objects
            for value in obj.values():
                find_reviews_recursive(value)

        elif isinstance(obj, list):
            for item in obj:
                find_reviews_recursive(item)

    try:
        find_reviews_recursive(data)
    except Exception as e:
        print(f"Error extracting reviews: {e}")
        import traceback
        traceback.print_exc()

    return reviews


def extract_review_details(value: Dict[str, Any], component: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract detailed information from a single review.

    Args:
        value: Review value dictionary
        component: Component dictionary containing tracking info

    Returns:
        Dictionary with extracted review details
    """
    # Extract basic review info
    review = {
        'review_id': value.get('id', ''),
        'author': value.get('author', ''),
        'certified_buyer': value.get('certifiedBuyer', False),
        'created_date': value.get('created', ''),
        'rating': value.get('rating', 0),
        'title': value.get('title', ''),
        'review_text': value.get('text', ''),
        'helpful_count': value.get('helpfulCount', 0),
    }

    # Extract location info
    location = value.get('location', {})
    if isinstance(location, dict):
        review['city'] = location.get('city', '')
        review['state'] = location.get('state', '')
    else:
        review['city'] = ''
        review['state'] = ''

    # Extract product attributes
    product_attrs = value.get('productAttributeList', [])
    if product_attrs:
        for attr in product_attrs:
            attr_name = attr.get('name', '').lower().replace(' ', '_')
            attr_value = attr.get('value', '')
            review[f'product_{attr_name}'] = attr_value

    # Extract image URLs
    images = value.get('images', [])
    image_urls = []
    for img in images:
        img_value = img.get('value', {})
        img_url = img_value.get('imageURL', '')
        if img_url:
            # Clean up the URL template
            img_url = img_url.replace('{@width}', '400').replace('{@height}', '400').replace('{@quality}', '90')
            image_urls.append(img_url)
    review['image_urls'] = ', '.join(image_urls) if image_urls else ''
    review['image_count'] = len(image_urls)

    # Extract votes
    upvote = value.get('upvote', {}).get('value', {})
    downvote = value.get('downvote', {}).get('value', {})
    review['upvotes'] = upvote.get('count', 0) if isinstance(upvote, dict) else 0
    review['downvotes'] = downvote.get('count', 0) if isinstance(downvote, dict) else 0

    # Extract verified purchase status
    review_props = value.get('reviewPropertyMap', {})
    review['verified_purchase'] = review_props.get('VERIFIED_PURCHASE', False)

    # Extract tracking info
    tracking = component.get('tracking', {})
    review['position'] = tracking.get('position', '')
    review['review_language'] = tracking.get('reviewLanguage', '')

    return review


def fetch_and_extract_reviews(url: str, params: dict, page_num: int = None) -> List[Dict[str, Any]]:
    """
    Fetch reviews from Flipkart and extract them with retry logic.

    Args:
        url: Product review URL
        params: Request parameters
        page_num: Optional page number for display

    Returns:
        List of extracted reviews
    """
    page_info = f" (Page {page_num})" if page_num else ""
    max_retries = 5
    retry_delay = 3  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                print(f"  Retry attempt {attempt}/{max_retries}...")
            else:
                print(f"Fetching reviews{page_info}...")

            response = requests.get(
                url,
                params=params,
                cookies=cookies,
                headers=headers,
                # proxies = PROXY_CONFIG,
                timeout=30
            )
            response.raise_for_status()

            print(f"Received response with status code: {response.status_code}")

            # Extract JSON from HTML
            data = extract_json_from_html(response.text)
            print("JSON data extracted successfully")

            # Extract reviews
            reviews = extract_reviews_from_json(data)
            print(f"Found {len(reviews)} reviews")

            return reviews

        except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"Connection error (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                import time
                time.sleep(retry_delay)
            else:
                print(f"Max retries reached. Giving up.")
                return []
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return []
        except ValueError as e:
            print(f"Error parsing response: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return []

    return []


def extract_product_id_from_url(url: str) -> Tuple[str, str, str]:
    """
    Extract product review URL and parameters from Flipkart product URL.

    IMPORTANT: Cleans URL to only keep essential parameters (pid, lid) to avoid
    Flipkart serving minimal page variants without reviews.

    Args:
        url: Flipkart product URL

    Returns:
        Tuple of (review_url, pid, lid) or (None, None, None) if extraction fails
    """
    try:
        from urllib.parse import urlparse, parse_qs

        # Simply replace /p/ with /product-reviews/
        if '/p/' in url:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)

            # Extract pid and lid - these are essential
            pid = query_params.get('pid', [None])[0]
            lid = query_params.get('lid', [None])[0]

            # Build clean URL with ONLY pid and lid parameters
            # Remove all tracking/search parameters to get full server-rendered page
            clean_query = []
            if pid:
                clean_query.append(f'pid={pid}')
            if lid:
                clean_query.append(f'lid={lid}')

            clean_query_string = '&'.join(clean_query) if clean_query else ''

            # Replace /p/ with /product-reviews/ in path
            clean_path = parsed.path.replace('/p/', '/product-reviews/')

            # Reconstruct clean URL
            review_url = f"{parsed.scheme}://{parsed.netloc}{clean_path}"
            if clean_query_string:
                review_url += f"?{clean_query_string}"

            return review_url, pid, lid
        else:
            print(f"Warning: Could not find /p/ in URL: {url}")
            return None, None, None

    except Exception as e:
        print(f"Error extracting product ID from URL {url}: {e}")
        return None, None, None


def scrape_product_reviews_wrapper(product_url: str, max_reviews: int = None) -> Tuple[List[Dict[str, Any]], int, bool]:
    """
    Wrapper function to scrape product reviews from a Flipkart URL.

    Args:
        product_url: Flipkart product URL
        max_reviews: Maximum number of reviews to scrape. If None, scrapes all reviews.

    Returns:
        Tuple of (reviews_list, review_count, success)
    """
    import time

    print(f"\n{'='*80}")
    print(f"Processing URL: {product_url}")
    if max_reviews:
        print(f"Max reviews limit: {max_reviews}")
    else:
        print(f"Max reviews limit: No limit (scraping all)")
    print(f"{'='*80}")

    try:
        # Extract product ID and build review URL
        review_url, _, _ = extract_product_id_from_url(product_url)

        if not review_url:
            print(f"✗ Failed to extract product ID from URL")
            return ([], 0, False)

        print(f"Review URL: {review_url}")

        # Build base URL without query parameters for pagination
        from urllib.parse import urlparse
        parsed = urlparse(review_url)
        base_review_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        product_reviews = []
        page = 1
        consecutive_empty_pages = 0
        max_consecutive_empty = 3

        while True:
            print(f"\n  Page {page}...", end=' ')

            params = {'page': str(page)}
            reviews = fetch_and_extract_reviews(base_review_url, params, page_num=page)

            if reviews:
                consecutive_empty_pages = 0

                # Check if adding these reviews would exceed max_reviews
                if max_reviews:
                    remaining_slots = max_reviews - len(product_reviews)
                    if remaining_slots <= 0:
                        print(f"✓ Max reviews limit reached ({len(product_reviews)} reviews)")
                        break
                    elif len(reviews) > remaining_slots:
                        # Only take the reviews we need to reach max_reviews
                        reviews = reviews[:remaining_slots]
                        product_reviews.extend(reviews)
                        print(f"✓ {len(reviews)} reviews extracted (reached max limit of {max_reviews})")
                        break

                product_reviews.extend(reviews)
                print(f"✓ {len(reviews)} reviews extracted (total: {len(product_reviews)})")
            else:
                consecutive_empty_pages += 1
                print(f"✗ No reviews")

                if consecutive_empty_pages >= max_consecutive_empty:
                    print(f"\n  Stopping after {consecutive_empty_pages} consecutive empty pages")
                    break

            # Safety limit
            if page >= 1000:
                print(f"\n  Reached safety limit of 1000 pages")
                break

            page += 1

            # Delay between requests
            if reviews:
                delay = 2.5
                time.sleep(delay)

        print(f"\n  Summary: {len(product_reviews)} total reviews extracted")
        return (product_reviews, len(product_reviews), True)

    except Exception as e:
        print(f"\n✗ Error scraping product: {e}")
        import traceback
        traceback.print_exc()
        return ([], 0, False)
