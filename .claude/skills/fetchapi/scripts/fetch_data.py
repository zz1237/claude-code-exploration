"""
Async API data fetching script using httpx.

This script fetches CSV data from multiple GitHub URLs and saves them locally,
with comprehensive logging of all operations.
"""

import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

import httpx


# Configure logging
def setup_logging():
    """Set up logging configuration with timestamp-based directory."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = Path(".claude/skills/fetchapi/logs") / timestamp
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "fetchapi.log"

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def extract_filename(url: str) -> str:
    """Extract filename from URL."""
    return url.split("/")[-1]


async def fetch_data_from_api(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> tuple[bool, str]:
    """
    Fetch data from a single API endpoint.

    Args:
        client: AsyncClient instance for making HTTP requests
        url: URL to fetch data from
        logger: Logger instance for logging operations

    Returns:
        Tuple of (success: bool, message: str)
    """
    filename = extract_filename(url)
    try:
        logger.info(f"Fetching data from: {url}")
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()

        # Create data directory with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        data_dir = Path(".claude/skills/fetchapi/data") / timestamp
        data_dir.mkdir(parents=True, exist_ok=True)

        # Save the CSV file
        file_path = data_dir / filename
        file_path.write_text(response.text)

        logger.info(f"Successfully saved {filename} to {file_path}")
        return True, f"Successfully fetched {filename}"

    except httpx.HTTPError as e:
        error_msg = f"HTTP error fetching {filename}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error fetching {filename}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg


async def main():
    """Main function to orchestrate API fetching."""
    logger = setup_logging()

    urls = [
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
        "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
    ]

    logger.info("=" * 60)
    logger.info("Starting API data fetch operation")
    logger.info(f"Total URLs to fetch: {len(urls)}")
    logger.info("=" * 60)

    async with httpx.AsyncClient() as client:
        tasks = [fetch_data_from_api(client, url, logger) for url in urls]
        results = await asyncio.gather(*tasks)

    # Log summary
    successful = sum(1 for success, _ in results if success)
    failed = len(results) - successful

    logger.info("=" * 60)
    logger.info("API Fetch Operation Summary")
    logger.info(f"Total requests: {len(results)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info("=" * 60)

    if failed > 0:
        logger.warning("Some API calls failed. Check the logs above for details.")
        return False

    logger.info("All API calls completed successfully!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
