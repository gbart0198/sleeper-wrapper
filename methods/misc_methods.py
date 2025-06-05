import requests
from typing import List, Optional

from models.league_state import LeagueState
from .helper_methods import make_request_and_cache


def get_trending_players(type: str, lookback_hours: str, limit: str) -> List[dict]:
    """
    Fetch trending players from a public API.

    Args:
        type (str): The type of trending data to fetch (e.g., 'waiver', 'trade').
        lookback_hours (str): The number of hours to look back for trends.
        limit (str): The maximum number of results to return.

    Returns:
        List[dict]: A list of trending players.
    """
    url = f"https://api.sleeper.app/v1/players/nfl/trending/{type}?lookback_hours={lookback_hours}&limit={limit}"
    try:
        # don't cache trending players as they change frequently
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data:
                print(f"ERROR: No trending players found for type: {type}")
                return []
            return data
        else:
            print(f"ERROR: Failed to fetch trending players from {url}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching trending players: {e}")
        return []


def get_nfl_state() -> Optional[LeagueState]:
    """
    Fetch the current NFL state from the public API.

    Returns:
        dict: The current NFL state.
    """
    url = "https://api.sleeper.app/v1/state/nfl"
    try:
        response = make_request_and_cache(url)
        if not response:
            print("ERROR: No NFL state data found.")
            return None
        print(response)
        return LeagueState.model_validate(response)
    except requests.RequestException as e:
        print(f"Error fetching NFL state: {e}")
        return None
