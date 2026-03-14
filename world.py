import random

import npc as n


game_state = {
    "player": {
        "name": "Héros",
        "hp": 20,
        "max_hp": 20,
        "strength": 3,
        "agility": 2,
        "intelligence": 1,
        "gold": 10,
        "status": []
    },
    "world": {
        "danger_level": 1,
        "war": False,
        "bandits_active": True,
        "economy": 1
    },
    "day": 1,
    "dungeon": None,
    "factions": {
        "royaume": {
            "reputation": 0,
            "power": 5
        },
        "bandits": {
            "reputation": 0,
            "power": 3
        },
        "mages": {
            "reputation": 0,
            "power": 4
        }
    },
    "npcs": [],
    "killed_npcs": [],
    "history": []
}


def update_world(game_state):
    world = game_state["world"]

    # le danger fluctue
    if random.random() < 0.3:
        world["danger_level"] += random.choice([-1, 1])

    world["danger_level"] = max(1, world["danger_level"])

    n.update_factions(game_state)
    n.update_npcs(game_state)