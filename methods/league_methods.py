from models import league_user
from models.league_user import LeagueUser
from models.roster import RosterResponse
from models.transaction import LeagueTransactionResponse
from .helper_methods import make_request_and_cache
import requests
from typing import List


def get_rosters_for_league(league_id: str) -> List[RosterResponse]:
    """
    Fetch rosters for a given league ID.

    Args:
        league_id (str): The league ID to fetch rosters for.

    Returns:
        List[dict]: A list of rosters associated with the league.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    try:
        response = make_request_and_cache(url)
        if not response:
            print(f"ERROR: No rosters found for league ID: {league_id}")
            return []
        return [RosterResponse.model_validate(roster) for roster in response]
    except requests.RequestException as e:
        print(f"Error fetching rosters for league ID {league_id}: {e}")
        return []


def get_users_for_league(league_id: str) -> List[LeagueUser]:
    """
    Fetch users for a given league ID.

    Args:
        league_id (str): The league ID to fetch users for.

    Returns:
        List[dict]: A list of users associated with the league.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    try:
        response = make_request_and_cache(url)
        league_users = []
        if not response:
            print(f"ERROR: No users found for league ID: {league_id}")
            return []
        for user in response:
            user_data = LeagueUser.model_validate(user)
            league_users.append(user_data)
        return league_users
    except requests.RequestException as e:
        print(f"Error fetching users for league ID {league_id}: {e}")
        return []


def get_matchups_for_league(league_id: str, week: str) -> List[dict]:
    """
    Fetch matchups for a given league ID and week.

    Args:
        league_id (str): The league ID to fetch matchups for.
        week (str): The week number to fetch matchups for.

    Returns:
        List[dict]: A list of matchups associated with the league and week.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
    try:
        response = make_request_and_cache(url)
        if not response:
            print(
                f"ERROR: No matchups found for league ID: {league_id} and week: {week}"
            )
            return []
        return response
    except requests.RequestException as e:
        print(f"Error fetching matchups for league ID {league_id} and week {week}: {e}")
        return []


def get_traded_picks_for_league(league_id: str) -> List[dict]:
    """
    Fetch traded picks for a given league ID.

    Args:
        league_id (str): The league ID to fetch traded picks for.

    Returns:
        List[dict]: A list of traded picks associated with the league.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/traded_picks"
    try:
        response = make_request_and_cache(url)
        if not response:
            print(f"ERROR: No traded picks found for league ID: {league_id}")
            return []
        return response
    except requests.RequestException as e:
        print(f"Error fetching traded picks for league ID {league_id}: {e}")
        return []


def get_transactions_for_league(
    league_id: str, week: int
) -> List[LeagueTransactionResponse]:
    """
    Fetch transactions for a given league ID and week.

    Args:
        league_id (str): The league ID to fetch transactions for.
        week (str): The week number to fetch transactions for.

    Returns:
        List[dict]: A list of transactions associated with the league and week.
    """
    url = f"https://api.sleeper.app/v1/league/{league_id}/transactions/{week}"
    try:
        response = make_request_and_cache(url)
        if not response:
            print(
                f"ERROR: No transactions found for league ID: {league_id} and week: {week}"
            )
            return []
        return [
            LeagueTransactionResponse.model_validate(transaction)
            for transaction in response
        ]
    except requests.RequestException as e:
        print(
            f"Error fetching transactions for league ID {league_id} and week {week}: {e}"
        )
        return []
