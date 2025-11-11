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

        flipkart_urls = actor_input.get('flipkart_urls', [])
        max_reviews = actor_input.get('max_reviews', 0)

        # Validate input
        if not flipkart_urls or len(flipkart_urls) == 0:
            Actor.log.error('Missing required input: flipkart_urls')
            await Actor.fail('Missing required input: flipkart_urls (must provide at least one URL)')
            return

        Actor.log.info(f'Starting scraper for {len(flipkart_urls)} URL(s)')

        # Set max_reviews to None if 0 or not set (scrape all)
        max_reviews_param = None if max_reviews == 0 else max_reviews

        if max_reviews_param:
            Actor.log.info(f'Max reviews limit per product: {max_reviews_param}')
        else:
            Actor.log.info('Max reviews limit: No limit (scraping all)')

        # Store all summaries and results
        all_summaries = []
        all_reviews = []
        total_reviews_scraped = 0
        successful_urls = 0
        failed_urls = []

        # Process each URL
        for idx, flipkart_url in enumerate(flipkart_urls, 1):
            Actor.log.info(f'\n{"="*60}')
            Actor.log.info(f'Processing URL {idx}/{len(flipkart_urls)}: {flipkart_url}')
            Actor.log.info(f'{"="*60}')

            # Validate URL format
            review_url, pid, lid = extract_product_id_from_url(flipkart_url)

            if not review_url:
                error_msg = f'Invalid Flipkart Product URL (missing /p/): {flipkart_url}'
                Actor.log.error(error_msg)
                failed_urls.append({'url': flipkart_url, 'error': 'Invalid URL format'})
                continue

            Actor.log.info(f'Product ID: {pid}')
            Actor.log.info(f'Review URL: {review_url}')

            # Scrape reviews
            try:
                reviews, review_count, success = scrape_product_reviews_wrapper(
                    flipkart_url,
                    max_reviews=max_reviews_param
                )

                if not success:
                    error_msg = f'Failed to scrape reviews for: {flipkart_url}'
                    Actor.log.error(error_msg)
                    failed_urls.append({'url': flipkart_url, 'error': 'Scraping failed'})
                    continue

                Actor.log.info(f'Successfully scraped {review_count} reviews from {flipkart_url}')

                # Create summary object
                summary = {
                    'flipkart_url': flipkart_url,
                    'product_id': pid,
                    'total_reviews': review_count,
                    'success': success,
                    'max_reviews_requested': max_reviews if max_reviews > 0 else 'all',
                    'url_index': idx
                }

                all_summaries.append(summary)

                # Push summary to dataset
                await Actor.push_data(summary)

                # Push each review to dataset with metadata
                for review in reviews:
                    review['flipkart_url'] = flipkart_url
                    review['product_id'] = pid
                    review['url_index'] = idx
                    await Actor.push_data(review)
                    all_reviews.append(review)

                total_reviews_scraped += review_count
                successful_urls += 1

                Actor.log.info(f'✓ Completed URL {idx}/{len(flipkart_urls)}')

            except Exception as e:
                error_msg = f'Error scraping reviews from {flipkart_url}: {str(e)}'
                Actor.log.exception(error_msg)
                failed_urls.append({'url': flipkart_url, 'error': str(e)})
                continue

        # Final summary
        Actor.log.info(f'\n{"="*60}')
        Actor.log.info('FINAL SUMMARY')
        Actor.log.info(f'{"="*60}')
        Actor.log.info(f'Total URLs processed: {len(flipkart_urls)}')
        Actor.log.info(f'Successful: {successful_urls}')
        Actor.log.info(f'Failed: {len(failed_urls)}')
        Actor.log.info(f'Total reviews scraped: {total_reviews_scraped}')

        if failed_urls:
            Actor.log.warning(f'\nFailed URLs:')
            for failed in failed_urls:
                Actor.log.warning(f"  - {failed['url']}: {failed['error']}")

        # Set final output
        final_output = {
            'total_urls': len(flipkart_urls),
            'successful_urls': successful_urls,
            'failed_urls': len(failed_urls),
            'total_reviews_scraped': total_reviews_scraped,
            'summaries': all_summaries,
            'failed_url_details': failed_urls
        }

        await Actor.set_value('OUTPUT', final_output)

        Actor.log.info('\nAll reviews pushed to dataset successfully')

        # If all URLs failed, mark the run as failed
        if successful_urls == 0:
            await Actor.fail('Failed to scrape any URLs')


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
