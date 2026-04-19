import random

import mecanics as m
import npc as n


event_bandit = {
    "text": "Un bandit surgit sur la route.",
    "condition": lambda gs:
        gs["player"]["location"] == "route"
        and gs["world"]["bandits_active"],
    "weight": 5,
    "choices": [
        {"text": "Combattre", "type": "combat"},
        {"text": "Négocier", "type": "test", "stat": "intelligence", "difficulty": 12}
    ]
}
event_bandit_ambush = {
    "text": "Des bandits te reconnaissent et attaquent.",
    "condition": lambda gs:
        gs["player"]["location"] == "route"
        and gs["factions"]["bandits"]["reputation"] <= -5,
    "weight": 4,
    "choices": [
        {"text": "Se battre", "type": "combat"}
    ]
}
event_traveler = {
    "text": "Un voyageur propose de partager un feu.",
    "condition": lambda gs: gs["player"]["hp"] < 15,
    "weight": 3,
    "choices": [
        {"text": "Accepter", "type": "test", "stat": "strength", "difficulty": 10},
        {"text": "Refuser", "type": "continuer"}
    ]
}
event_ruins = {
    "text": "Tu découvres des ruines anciennes.",
    "condition": lambda gs:
        gs["player"]["location"] == "ruines"
        and True,
    "weight": 2,
    "choices": [
        {"text": "Explorer", "type": "enter_dungeon"}
    ]
}
event_royal_help = {
    "text": "Un garde royal t'offre son aide.",
    "condition": lambda gs:
        gs["player"]["location"] in ["route", "village"]
        and gs["factions"]["royaume"]["reputation"] >= 5,
    "weight": 2,
    "choices": [
        {"text": "Accepter", "type": "heal"}
    ]
}
event_rumor = {
    "text": "Quelqu’un parle de tes exploits récents.",
    "condition": lambda gs: any(
        m["importance"] >= 3 for m in gs["history"]
    ),
    "weight": 2,
    "choices": [
        {"text": "Écouter", "type": "hear_rumor"}
    ]
}


STATIC_EVENTS = [
    event_bandit,
    event_bandit_ambush,
    event_traveler,
    event_ruins,
    event_royal_help,
    event_rumor
]


def get_all_events(game_state):
    events = []

    # événements fixes
    events.extend(STATIC_EVENTS)
    # événements dynamiques PNJ
    events.extend(generate_npc_events(game_state))

    return events


def generate_npc_events(game_state):
    events = []
    player_loc = game_state["player"]["location"]

    for npc in game_state["npcs"]:
        if npc["alive"] and npc["location"] == player_loc:
            events.append(npc_encounter_event(npc, player_loc))

    return events


def npc_encounter_event(npc, location):
    return {
        "text": f"Tu rencontres {npc['name']} : {location}.",
        "condition": lambda gs, n=npc: (
            n["alive"]
            and gs["day"] - n["last_seen_day"] > 2
        ),
        "weight": 2,
        "npc": npc,  # IMPORTANT
        "choices": n.generate_npc_choices(npc)
    }


def killed_npc(game_state, npc):
    event = {
        "type": "npc_killed",
        "npc": npc.name,
        "location": npc.location,
        "faction": npc.faction
    }

    game_state["killed_npcs"].append(event)

    for npc_other in game_state["npcs"]:
        if npc_other["faction"] == npc["faction"]:
            npc_other["relation_player"] -= npc_other["traits"]["loyal"]
        
        n.react_to_world_event(npc, event)


def choose_event(game_state, events):
    valid_events = [
        e for e in events
        if e["condition"](game_state)
    ]

    if not valid_events:
        return {
            "text": "La journée passe sans incident.",
            "choices": []
        }

    weights = [e["weight"] for e in valid_events]

    return random.choices(valid_events, weights=weights)[0]


def play_event(game_state, event):
    print(event["text"])

    for i, choice in enumerate(event["choices"]):
        print(f"{i+1}. {choice['text']}")

    selection = int(input("> ")) - 1
    m.resolve_choice(game_state, event, event["choices"][selection])