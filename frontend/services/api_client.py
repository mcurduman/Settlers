import requests
from utils.config import API_URL


def start_game(difficulty):
    return requests.post(
        f"{API_URL}/start-game", params={"difficulty": difficulty}
    ).json()


def get_state():
    return requests.get(f"{API_URL}/game-state").json()
