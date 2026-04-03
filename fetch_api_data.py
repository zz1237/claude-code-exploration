import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

import httpx

URLS = [
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_customer.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_store.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_date.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/dim_product.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_sales.csv",
    "https://raw.githubusercontent.com/anshlambagit/AnshLambaYoutube/refs/heads/main/DBT_Masterclass/fact_returns.csv",
]


def make_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def setup_logging(log_base_dir: Path) -> Path:
    timestamped_log_dir = log_base_dir / make_timestamp()
    timestamped_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = timestamped_log_dir / "fetchapi.log"

    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Starting fetchapi run")
    return log_file


async def fetch_and_save(url: str, data_dir: Path) -> None:
    file_name = Path(url).name
    target_file = data_dir / file_name

    async with httpx.AsyncClient(timeout=60.0) as client:
        logging.info("Fetching URL: %s", url)
        try:
            response = await client.get(url)
            response.raise_for_status()
            target_file.write_bytes(response.content)
            logging.info("Saved data to %s", target_file)
        except httpx.HTTPStatusError as exc:
            logging.error("HTTP error for %s - status %s", url, exc.response.status_code)
            raise
        except Exception as exc:
            logging.error("Error fetching %s: %s", url, exc)
            raise


async def main() -> None:
    data_base_dir = Path(".claude/skills/fetchapi/data")
    log_base_dir = Path(".claude/skills/fetchapi/logs")

    data_dir = data_base_dir / make_timestamp()
    data_dir.mkdir(parents=True, exist_ok=True)

    log_file = setup_logging(log_base_dir)
    logging.info("Data output directory: %s", data_dir)
    logging.info("Log file: %s", log_file)

    errors = []

    for url in URLS:
        try:
            await fetch_and_save(url, data_dir)
            logging.info("Success: %s", url)
        except Exception as exc:
            errors.append((url, str(exc)))
            logging.warning("Failure: %s - %s", url, exc)

    if errors:
        logging.error("Fetch run completed with errors: %s", errors)
        print("Completed with errors. Check log", log_file)
    else:
        logging.info("Fetch run completed successfully")
        print("Fetch completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
