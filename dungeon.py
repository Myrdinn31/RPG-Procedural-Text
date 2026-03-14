import random

import mecanics as m
import fight as f


ROOM_TYPES = [
    "combat",
    "treasure",
    "event",
    "trap",
    "rest"
]


def generate_dungeon(length):
    dungeon = {
        "rooms": [],
        "current_room": 0,
        "danger": 1
    }

    for i in range(length):
        room = {
            "type": random.choice(ROOM_TYPES),
            "cleared": False
        }
        dungeon["rooms"].append(room)

    return dungeon


def explore_dungeon(game_state):
    dungeon = game_state["dungeon"]

    while dungeon["current_room"] < len(dungeon["rooms"]):
        room = dungeon["rooms"][dungeon["current_room"]]
        resolve_room(game_state, room)

        dungeon["current_room"] += 1

    m.add_memory(
        game_state,
        "dungeon_cleared",
        "Un ancien donjon a été exploré.",
        ["player"],
        importance=3
    )

    print("Tu trouves la sortie du donjon.")
    game_state["dungeon"] = None


def resolve_room(game_state, room):
    player = game_state["player"]

    print("\n--- Nouvelle salle ---")

    if room["type"] == "combat":
        f.combat(player, {
            "name": "Créature des ruines",
            "hp": 6 + game_state["dungeon"]["danger"] * 2,
            "attack": 2,
            "faction": "dungeon"
        }, game_state)
    elif room["type"] == "treasure":
        gold = random.randint(1,10)
        player["gold"] += gold
        print(f"Tu trouves {gold} or.")
    elif room["type"] == "trap":
        m.damage_player(player, random.randint(1,3), game_state)
        print("Un piège se déclenche !")
    elif room["type"] == "rest":
        heal = random.randint(1,5)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        print(f"Tu te reposes. Tu as maintenant {player['hp']} HP.")
    elif room["type"] == "event":
        print("Un mystère ancien t'observe...")

    game_state["dungeon"]["danger"] += 1