import requests
import json
import logging
import os


next_page_url = os.getenv("API_URL")

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_all_characters(next_page_url=next_page_url):
    logger.info("Start Fetching all characters")
    while next_page_url:
        try:
            response = requests.get(next_page_url)
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            logger.exception(f"Request to {next_page_url} failed: {err}")

        data = response.json()
       # print(f"Total characters: {data.get("info").get("count", "Unknown")}")

        next_page_url = data.get("info").get("next")

        if next_page_url:
            logger.info("Continue fetching next page...")

    return True


get_all_characters()
