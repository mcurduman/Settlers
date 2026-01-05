import requests
from utils.config import API_URL


def start_game(difficulty):
    return requests.post(
        f"{API_URL}/game/start", params={"difficulty": difficulty}
    ).json()


def get_state():
    return requests.get(f"{API_URL}/game/state").json()


def roll_dice():
    result = requests.post(f"{API_URL}/game/roll-dice").json()
    print(result)
    return result


def place_settlement(position):
    return requests.post(
        f"{API_URL}/game/place-settlement", json={"position": position}
    ).json()


def place_road(start, end):
    return requests.post(
        f"{API_URL}/game/place-road", json={"a": start, "b": end}
    ).json()
