import requests
from prefect import flow, task
from datetime import timedelta
import json
import argparse
from urllib.parse import urlparse


@task(
    name="Fetch Data",
    description="Fetch data from the specified API endpoint, with retries on failure.",
    retries=3,
    retry_delay_seconds=10,
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
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@task(name="Process Data", description="Process the fetched data to extract results.")
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
    return data["results"]


@task(
    name="Generate Filename",
    description="Generate a sequential filename based on the endpoint.",
    tags=["filename", "generate"],
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


@task(name="Save Data", description="Save the processed data.", tags=["save", "data"])
def save_data(data: list, filename: str = "data.json"):
    """
    Save the processed data.

    Args:
        data (list): The processed data to be saved.

    Returns:
        None
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


@flow(
    name="Rick and Morty Flow",
    description="A flow to fetch, process, and save data from the Rick and Morty API.",
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
        description="Script para executar o fluxo Prefect com a URL da API como parâmetro."
    )
    parser.add_argument(
        "--url", default="https://rickandmortyapi.com/api/character", help="URL da API"
    )
    args = parser.parse_args()
    api_flow(args.url)
