import os
import sys
from typing import Optional
from dotenv import load_dotenv
from methods.league_methods import (
    get_rosters_for_league,
    get_transactions_for_league,
    get_users_for_league,
)
from methods.misc_methods import get_nfl_state
from models.league import LeagueResponse
from models.league_state import LeagueState
from models.league_user import LeagueUser
from models.user import UserResponse
from utils import RequestCache, PlayerData
from methods import get_user_data, get_leagues_for_user
from utils.player_mapper import PlayerMapper


def main():
    cache = RequestCache()
    player_mapper = PlayerMapper()

    cache.load()

    user_data: Optional[UserResponse] = None
    selected_league: Optional[LeagueResponse] = None
    league_state: Optional[LeagueState] = None

    try:
        load_dotenv()
        username = os.getenv("username")
        if not username:
            print("username not set in .env, using command line argument if provided.")
            if len(sys.argv) != 2:
                print("Usage: python main.py <username>")
                print("ERROR: Please provide a username or set username in .env")
                return
            username = sys.argv[1].strip()
        else:
            print(f"Using username from .env: {username}")

        # -------- Main Logic --------
        user_data = get_user_data(username)
        user_id = user_data.user_id if user_data else None
        if not user_id:
            print(f"ERROR: No user ID found for username: {username}")
            return
        leagues = get_leagues_for_user(user_id)
        league_state = get_nfl_state()

        print("Which league would you like to view?:")
        for i in range(len(leagues)):
            print(
                f"[{i + 1}] - League Name: {leagues[i].name}, ID: {leagues[i].league_id}"
            )

        league_id = input("> ").strip()
        if (
            not league_id.isdigit()
            or int(league_id) < 1
            or int(league_id) > len(leagues)
        ):
            print("ERROR: Invalid league selection.")
            return

        selected_league = leagues[int(league_id) - 1]

    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)
    finally:
        cache.save()

    assert user_data, "User data should not be empty"
    assert selected_league, "Selected league should not be empty"
    assert league_state, "League state should not be empty"

    while True:
        print("\nOptions:")
        print("[1] - List My Roster")
        print("[2] - List All Rosters in League")
        print("[2] - List Other Users in League")
        print("[3] - List Transactions in League")
        print("[q] - Exit the program")
        choice = input("Enter your choice: ").strip()
        print("\n" + "=" * 40 + "\n")

        if choice == "1":
            rosters = get_rosters_for_league(selected_league.league_id)
            if not rosters:
                print("No rosters found for this league.")
                continue

            my_roster = next(
                (roster for roster in rosters if roster.owner_id == user_data.user_id),
                None,
            )
            if not my_roster:
                print("No roster found for your user ID in this league.")
                continue

            print(f"My Roster for League ID {selected_league.league_id}:")
            print(f"Roster ID: {my_roster.roster_id}, Owner ID: {my_roster.owner_id}")
            print(f"Starters: {my_roster.get_mapped_starters(player_mapper)}")
            print(f"Reserve: {my_roster.get_mapped_reserve(player_mapper)}")
            print(f"Players: {my_roster.get_mapped_players(player_mapper)}")
            print(f"Settings: {my_roster.settings}")
            print("-" * 40)

        elif choice == "2":
            rosters = get_rosters_for_league(selected_league.league_id)
            if not rosters:
                print("No rosters found for this league.")
                continue
            print(f"Rosters for League ID {selected_league.league_id}:")
            for roster in rosters:
                print(
                    f"Roster ID: {roster.roster_id}, Owner ID: {roster.owner_id}, League ID: {roster.league_id}"
                )
                print(f"Starters: {roster.starters}")
                print(f"Reserve: {roster.reserve}")
                print(f"Players: {roster.players}")
                print(f"Settings: {roster.settings}")
                print("-" * 40)

        elif choice == "3":
            users = get_users_for_league(selected_league.league_id)
            if not users:
                print("No users found in this league.")
                continue

            print("Users in the selected league:")
            for user in users:
                print(f"User ID: {user.user_id}, Display Name: {user.display_name}")
        elif choice == "4":
            transactions = get_transactions_for_league(
                selected_league.league_id, league_state.week
            )
            if not transactions:
                print("No transactions found for this league.")
                continue

            print(
                f"Transactions for League ID {selected_league.league_id} in Week {league_state.week}:"
            )
            for transaction in transactions:
                print(
                    f"Transaction ID: {transaction.transaction_id}, Type: {transaction.type}, Status: {transaction.status}, Created: {transaction.created}"
                )
                print(f"Roster IDs: {transaction.roster_ids}")
                if transaction.drops:
                    print(f"Drops: {transaction.drops}")
                if transaction.adds:
                    print(f"Adds: {transaction.adds}")
                if transaction.draft_picks:
                    print("Draft Picks:")
                    for pick in transaction.draft_picks:
                        print(
                            f"  Season: {pick.season}, Round: {pick.round}, Owner ID: {pick.owner_id}"
                        )
        elif choice.lower() == "q":
            print("Exiting the program.")
            break
        else:
            print(f"Invalid choice: {choice}")
            print("Invalid choice, please try again.")
        print("\n" + "=" * 40 + "\n")

    cache.save()


if __name__ == "__main__":
    main()
