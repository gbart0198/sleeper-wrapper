import json
from pathlib import Path
import sys


class RequestCache:
    _instance = None
    _cache = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __contains__(self, key):
        return key in self._cache

    def __getitem__(self, key):
        return self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value

    def load(self, path: str = "./data/_request_cache.json"):
        print(f"Loading cache from {path}")
        try:
            file = Path(path)
            if file.exists():
                with open(path, "r") as f:
                    self._cache = json.load(f)
        except Exception as e:
            print(f"ERROR: Failed to load cache from {path}, exiting. Exception: {e}")
            sys.exit(1)

    def save(self, path: str = "./data/_request_cache.json"):
        print(f"Saving cache to {path}")
        with open(path, "w+") as f:
            json.dump(self._cache, f, indent=2)
