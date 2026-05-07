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
event_rumor_player = {
    "text": "Quelqu’un parle de tes exploits récents.",
    "condition": lambda gs: any(
        m["importance"] >= 3 for m in gs["history"]
    ),
    "weight": 2,
    "choices": [
        {"text": "Écouter", "type": "hear_rumor_player"}
    ]
}
event_rumors = {
    "text": "Tu entends des rumeurs dans les environs.",
    "condition": lambda gs: True,
    "weight": 2,
    "choices": [
        {"text": "Écouter", "type": "hear_rumor"}
    ]
}
event_quest_offer = {
    "text": "Quelqu’un te propose une mission.",
    "condition": lambda gs: len(gs["quests"]) > 0,
    "weight": 2,
    "choices": [
        {"text": "Voir les quêtes", "type": "show_quests"}
    ]
}


STATIC_EVENTS = [
    event_bandit,
    event_bandit_ambush,
    event_traveler,
    event_ruins,
    event_royal_help,
    event_rumor_player,
    event_rumors,
    event_quest_offer
]

ACTIONS = [
    "attack", "help", "betray", "reveal", "steal",
    "protect", "guide", "ambush", "escape", "observe"
]

SUBJECTS = [
    "bandits", "a merchant", "a ruin", "a secret",
    "a faction", "a creature", "an artifact"
]

DESCRIPTORS = [
    "hidden", "dangerous", "ancient", "cursed",
    "unexpected", "hostile", "valuable"
]


EVENT_FOCUS = [
    "remote_event",        # ailleurs dans le monde
    "ambiguous_event",     # flou/interprétable
    "new_npc",             # nouveau personnage
    "npc_action",          # action d’un PNJ existant
    "npc_negative",
    "npc_positive",
    "toward_thread",       # vers une quête
    "away_thread",         # détourne d’une quête
    "close_thread",        # résout une quête
    "player_negative",
    "player_positive",
    "current_context"      # basé sur la scène actuelle
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
        "npc": npc["name"],
        "location": npc["location"],
        "faction": npc["faction"]
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


def get_weighted_event_focus(game_state):
    weights = {
        "current_context": 5,
        "npc_action": 4,
        "toward_thread": 3,
        "npc_negative": 3,
        "npc_positive": 3,
        "new_npc": 2,
        "remote_event": 2,
        "ambiguous_event": 1,
        "close_thread": 1
    }

    # si joueur en combat → favoriser contexte
    if game_state["in_combat"]:
        weights["current_context"] += 3

    return weighted_random(weights)


def get_context(game_state):
    return {
        "location": game_state["player"]["location"],
        "npcs_here": [...],
        "active_quests": game_state["quests"],
        "factions": ...
    }


def generate_random_event(game_state):
    focus = get_weighted_event_focus(game_state)

    action = random.choice(ACTIONS)
    subject = random.choice(SUBJECTS)
    descriptor = random.choice(DESCRIPTORS)

    return {
        "focus": focus,
        "action": action,
        "subject": subject,
        "descriptor": descriptor
    }


def interpret_event(event, game_state):
    focus = event["focus"]

    if focus == "current_context":
        return interpret_context_event(event, game_state)
    elif focus == "npc_action":
        return interpret_npc_action(event, game_state)
    elif focus == "new_npc":
        return spawn_new_npc(event)
    elif focus == "remote_event":
        return trigger_remote_event(event)
    
    return event


def create_event(text, choices):
    return {
        "text": text,
        "choices": choices
    }


def generate_playable_random_event(game_state):
    raw_event = generate_random_event(game_state)

    return build_event_from_meaning(raw_event, game_state)


def build_event_from_meaning(event, game_state):
    focus = event["focus"]
    action = event["action"]
    subject = event["subject"]

    if focus == "current_context":
        return handle_context_event(action, subject, game_state)
    
    if focus == "npc_action":
        return handle_npc_event(action, subject, game_state)
    
    if focus == "npc_negative":
        return handle_npc_negative(action, subject, game_state)

    if focus == "npc_positive":
        return handle_npc_positive(action, subject, game_state)

    if focus == "new_npc":
        return handle_new_npc(game_state)

    if focus == "toward_thread":
        return handle_thread_progress(game_state)

    if focus == "remote_event":
        return handle_remote_event(game_state)

    return fallback_event()


def handle_npc_negative(action, subject, game_state):
    if subject == "bandits" and action == "betray":
        bandit = get_random_bandit(game_state)

        return create_event(
            f"Un bandit trahit son groupe et attaque ses alliés !",
            [
                {"text": "Profiter du chaos pour attaquer", "type": "combat_advantage"},
                {"text": "Observer", "type": "wait"},
                {"text": "Fuir", "type": "escape"}
            ]
        )
    

def handle_npc_positive(action, subject, game_state):
    if action == "help":
        npc = create_npc("Voyageur")

        return create_event(
            f"Un voyageur intervient pour t'aider !",
            [
                {"text": "Accepter son aide", "type": "gain_ally", "npc": npc},
                {"text": "Refuser", "type": "ignore"}
            ]
        )
    

def handle_thread_progress(game_state):
    quest = get_active_quest(game_state)

    return create_event(
        f"Tu découvres un indice lié à {quest['description']}.",
        [
            {"text": "Suivre la piste", "type": "advance_quest"},
            {"text": "Ignorer", "type": "ignore"}
        ]
    )


def handle_remote_event(game_state):
    return create_event(
        "Une rumeur parle d'un village attaqué au loin.",
        [
            {"text": "Enquêter", "type": "new_quest"},
            {"text": "Ignorer", "type": "ignore"}
        ]
    )


def handle_context_event(action, subject, game_state):
    if action == "ambush":
        return create_event(
            "Les bandits lancent une embuscade !",
            [
                {"text": "Combattre", "type": "combat_hard"},
                {"text": "Fuir", "type": "escape"},
                {"text": "Se cacher", "type": "stealth"}
            ]
        )
    

def fallback_event():
    return create_event(
        "Quelque chose d'étrange se produit, sans conséquence immédiate.",
        [{"text": "Continuer", "type": "continue"}]
    )