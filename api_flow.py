import requests
from prefect import flow, task
from datetime import timedelta
import json
import argparse
from urllib.parse import urlparse
from prefect import flow, get_run_logger
import os


@task(
    name="Fetch Data",
    description="Fetch data from the specified API endpoint, with retries on failure.",
    retries=os.environ.get("TASK_RETRIES"),
    retry_delay_seconds=os.environ.get("TASK_RETRY_DELAY"),
    cache_expiration=timedelta(minutes=5),
)
def fetch_data(url: str) -> dict:
    """
    Fetch data from the specified API endpoint.

    Args:
        url (str): The API endpoint URL.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    try:
        response = requests.get(url,timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger = get_run_logger()
        if e.response.status_code == 404:
            logger.warning(f"{e.response.status_code} - URL not found: {url}")
        elif e.response.status_code == 500:
            logger.error(f"{e.response.status_code} - Server error: {url}")
        else:
            logger.error(f"{e.response.status_code} -Erro HTTP: {url}")
        raise SystemExit(e)
    except requests.exceptions.Timeout:
        logger = get_run_logger()
        logger.error(f"Timeout occurred while fetching data from {url}")
        raise


@task(
    name="Process Data",
    description="Process the fetched data to extract results.",
    retries=os.environ.get("TASK_RETRIES"),
    retry_delay_seconds=os.environ.get("TASK_RETRY_DELAY"),
    cache_expiration=timedelta(minutes=5),
)
def process_data(data: dict) -> list:
    """
    Process the fetched data to extract results.

    Args:
        data (dict): The JSON data fetched from the API.

    Returns:
        list: The list of results from the JSON data.

    Raises:
        KeyError: If the 'results' key is not found in the data.
    """
    return data


@task(
    name="Generate Filename",
    description="Generate a sequential filename based on the endpoint.",
    tags=["filename", "generate"],
    retries=os.environ.get("TASK_RETRIES"),
    retry_delay_seconds=os.environ.get("TASK_RETRY_DELAY"),
    cache_expiration=timedelta(minutes=5),
)
def generate_filename(
    url: str,
) -> str:
    """
    Generate a filename based on the endpoint.

    Args:
        endpoint (str): The API endpoint.

    Returns:
        str: The generated filename.
    """

    parsed_url = urlparse(url)
    endpoint = parsed_url.path.replace("/api/", "")
    endpoint = endpoint.replace("/", "_").replace(".", "_").replace(",", "_")
    filename = endpoint + ".json"

    return filename


@task(
    name="Save Data",
    description="Save the processed data.",
    tags=["save", "data"],
    retries=os.environ.get("TASK_RETRIES"),
    retry_delay_seconds=os.environ.get("TASK_RETRY_DELAY"),
    cache_expiration=timedelta(minutes=5),
)
def save_data(data: list, filename: str = "data.json"):
    """
    Save the processed data.

    Args:
        data (list): The processed data to be saved.

    Returns:
        None
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logger = get_run_logger()
        logger.info(f"Data saved to {filename}")
    except IOError as e:
        logger = get_run_logger()
        logger.error(f"Error saving file: {e}")
        raise
    except json.JSONEncodeError as e:
        logger = get_run_logger()
        logger.error(f"Error serializing data to JSON: {e}")
        raise


@flow(
    name="Rick and Morty Flow",
    description="A flow to fetch, process, and save data from the Rick and Morty API.",
    retries=os.environ.get("TASK_RETRIES"),
    retry_delay_seconds=os.environ.get("TASK_RETRY_DELAY"),
)
def api_flow(url):
    """
    The main flow to fetch, process, and save data from the Rick and Morty API.

    Steps:
        1. Fetch data from the API.
        2. Process the fetched data.
        3. Generate a filename based on the endpoint.
        4. Save the processed data.
    """
    # url = "https://rickandmortyapi.com/api/character"
    data = fetch_data(url)
    processed_data = process_data(data)
    filename = generate_filename(url)
    save_data(processed_data, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to run the Prefect flow with the API URL as a parameter."
    )
    parser.add_argument("--url", default=os.environ.get("API_URL"), help="URL da API")
    args = parser.parse_args()
    api_flow(args.url)
