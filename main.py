#!/usr/bin/env python3
"""
Apify Actor entry point for Flipkart Review Scraper
"""

from apify import Actor
from flipkart_scraper_apify import (
    extract_product_id_from_url,
    scrape_product_reviews_wrapper
)


async def main():
    """
    Main function for Apify Actor.
    Reads input from Apify, scrapes reviews, and pushes results to dataset.
    """
    async with Actor:
        # Get input from Apify
        actor_input = await Actor.get_input() or {}

        flipkart_url = actor_input.get('flipkart_url')
        max_reviews = actor_input.get('max_reviews', 0)

        # Validate input
        if not flipkart_url:
            Actor.log.error('Missing required input: flipkart_url')
            await Actor.fail('Missing required input: flipkart_url')
            return

        Actor.log.info(f'Starting scraper for URL: {flipkart_url}')

        # Validate URL format
        review_url, pid, lid = extract_product_id_from_url(flipkart_url)

        if not review_url:
            error_msg = 'Invalid Flipkart Product URL (missing /p/)'
            Actor.log.error(error_msg)
            await Actor.fail(error_msg)
            return

        Actor.log.info(f'Product ID: {pid}')
        Actor.log.info(f'Review URL: {review_url}')

        # Set max_reviews to None if 0 or not set (scrape all)
        max_reviews_param = None if max_reviews == 0 else max_reviews

        if max_reviews_param:
            Actor.log.info(f'Max reviews limit: {max_reviews_param}')
        else:
            Actor.log.info('Max reviews limit: No limit (scraping all)')

        # Scrape reviews
        try:
            reviews, review_count, success = scrape_product_reviews_wrapper(
                flipkart_url,
                max_reviews=max_reviews_param
            )

            if not success:
                error_msg = 'Failed to scrape reviews'
                Actor.log.error(error_msg)
                await Actor.fail(error_msg)
                return

            Actor.log.info(f'Successfully scraped {review_count} reviews')

            # Create summary object
            summary = {
                'flipkart_url': flipkart_url,
                'product_id': pid,
                'total_reviews': review_count,
                'success': success,
                'max_reviews_requested': max_reviews if max_reviews > 0 else 'all'
            }

            # Push summary to dataset
            await Actor.push_data(summary)

            # Push each review to dataset
            for review in reviews:
                # Add metadata to each review
                review['flipkart_url'] = flipkart_url
                review['product_id'] = pid
                await Actor.push_data(review)

            Actor.log.info('All reviews pushed to dataset successfully')

            # Set output
            await Actor.set_value('OUTPUT', {
                'summary': summary,
                'reviews': reviews
            })

        except Exception as e:
            error_msg = f'Error scraping reviews: {str(e)}'
            Actor.log.exception(error_msg)
            await Actor.fail(error_msg)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
