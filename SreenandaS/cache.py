import json
import os

CACHE_FILE = "cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r") as file:
        return json.load(file)


def save_cache(cache):

    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file, indent=4)