import json
from pathlib import Path
import sys


class PlayerData:
    _instance = None
    _store = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __contains__(self, key):
        return key in self._store

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value

    def load(self, path: str = "./data/player_json.json"):
        try:
            print(f"Loading player_json from {path}")
            file = Path(path)
            if file.exists():
                with open(path, "r") as f:
                    self._store = json.load(f)
        except Exception as e:
            print(
                f"ERROR: Failed to load player_json from {path}, exiting. Exception: {e}"
            )
            sys.exit(1)
