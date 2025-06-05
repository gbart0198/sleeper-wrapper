import json
from utils import RequestCache
import requests
from typing import Any


def make_request_and_cache(url: str) -> Any:
    """
    Make a request to the given URL and cache the response.

    Args:
        url (str): The URL to make the request to.

    Returns:
        dict: The JSON response from the request.
    """
    cache = RequestCache()
    if url in cache:
        print(f"Using cached data for {url}")
        return cache[url]

    print(f"Fetching data from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cache[url] = data
        return data
    else:
        print(f"ERROR: Failed to fetch data from {url}")
        return {}


def load_player_json() -> dict:
    """
    Load player data from a local JSON file.

    Returns:
        dict: The player data loaded from the JSON file.
    """
    try:
        with open("players.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("ERROR: players.json file not found.")
        return {}


def load_request_cache() -> dict:
    """
    Load request cache from a local JSON file.

    Returns:
        dict: The request cache loaded from the JSON file.
    """
    try:
        with open("request_cache.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("ERROR: request_cache.json file not found.")
        return {}
