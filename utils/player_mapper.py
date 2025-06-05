import json

class PlayerMapper:
    player_data = {}

    def __init__(self):
        with open("data/_player_data.json", "r") as f:
            self.player_data = json.load(f)

    def map_players(self, player: str) -> str:
        """
        Maps a player ID to a string representation.

        Args:
            player (int): The player ID to map.

        Returns:
            str: The string representation of the player ID.
        """

        if not player:
            return "No Player"
        if player in self.player_data:
            return (
                self.player_data[player]["first_name"] + " " + self.player_data[player]["last_name"]
            )
        return f"Player-{player}" if player else "No Player"
