import requests

from models.league import LeagueResponse
from models.user import UserResponse
from .helper_methods import make_request_and_cache
from typing import List, Optional


def get_user_data(username: str) -> Optional[UserResponse]:
    """
    Fetch user data from a public API.

    Args:
        username (str): The username to fetch data for.

    Returns:
        dict: The user data retrieved from the API.
    """
    url = f"https://api.sleeper.app/v1/user/{username}"
    try:
        response = make_request_and_cache(url)
        if not response:
            print(f"ERROR: No data found for username: {username}")
            return None
        return UserResponse.model_validate(response)
    except requests.RequestException as e:
        print(f"Error fetching data for {username}: {e}")
        return None


def get_leagues_for_user(user_id: str) -> List[LeagueResponse]:
    """
    Fetch leagues for a given user ID.

    Args:
        user_id (str): The user ID to fetch leagues for.

    Returns:
        List[dict]: A list of leagues associated with the user.
    """
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/2025"
    try:
        response = make_request_and_cache(url)
        leagues = []
        if not response:
            print(f"ERROR: No leagues found for user ID: {user_id}")
            return leagues
        for league in response:
            league_data = LeagueResponse.model_validate(league)
            leagues.append(league_data)
        return leagues
    except requests.RequestException as e:
        print(f"Error fetching leagues for user ID {user_id}: {e}")
        return []
