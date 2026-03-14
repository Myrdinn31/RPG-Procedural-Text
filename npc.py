import random

import event as e
import mecanics as m


enemy = {
    "name": "Bandit",
    "faction": "bandits",
    "hp": 10,
    "attack": 2
}


faction_relations = {
    "royaume": {"bandits": -5, "mages": 2},
    "bandits": {"royaume": -5},
    "mages": {"royaume": 2}
}


def create_npc(name):
    return {
        "name": name,
        "hp": 10,
        "location": "route",
        "goal": random.choice(["gain_gold", "explore", "survive"]),
        "faction": random.choice(["bandits", "royaume", "mages"]),
        "gold": 0,
        "alive": True,
        "relation_player": 0,
        "relationships": {},
        "last_seen_day": -999,
        "memories": [],
        "traits": {
            "brave": random.randint(0, 5),
            "greedy": random.randint(0, 5),
            "loyal": random.randint(0, 5),
            "aggressive": random.randint(0, 5)
        },
        "emotions": {
            "joy": 0,
            "anger": 0,
            "fear": 0,
            "sadness": 0,
            "trust": 0
        }
    }


def change_reputation(game_state, faction, amount):
    rep = game_state["factions"][faction]["reputation"]
    rep += amount
    game_state["factions"][faction]["reputation"] = rep

    print(f"Réputation avec {faction}: {rep}")


def update_factions(game_state):
    for faction in game_state["factions"].values():
        if random.random() < 0.2:
            faction["power"] += random.choice([-1, 1])

        faction["power"] = max(1, faction["power"])


def update_npcs(game_state):
    for npc in game_state["npcs"]:
        if not npc["alive"]:
            continue

        decay_emotions(npc)

        print(f"{npc['name']} => lieu : {npc['location']} / HP : {npc['hp']} / Goal : {npc['goal']} / Faction : {npc['faction']} / Gold : {npc['gold']} / Relation : {npc['relation_player']} / Brave : {npc['traits']['brave']} / Greedy : {npc['traits']['greedy']} / Loyal : {npc['traits']['loyal']} / Aggressive : {npc['traits']['aggressive']} / Joy : {npc['emotions']['joy']} / Anger : {npc['emotions']['anger']} / Fear : {npc['emotions']['fear']} / Sadness : {npc['emotions']['sadness']} / Trust : {npc['emotions']['trust']}")
        
        action = npc_choose_action(npc, game_state)
        resolve_npc_action(npc, action, game_state)

        if npc["hp"] <= 0:
            e.killed_npc(game_state, npc)


def npc_choose_action(npc, game_state):
    traits = npc["traits"]

    # S'il se souvient avoir été aidé
    if any(m["type"] == "helped_by_player" for m in npc["memories"]):
        if npc["relation_player"] > 5:
            return "assist_player"

    # Si agressif élevé → tendance combat
    if traits["aggressive"] > 3:
        return "fight"

    # Si cupide → cherche or
    if traits["greedy"] > 3:
        return "trade"

    # Si loyal et relation positive → aide joueur
    if traits["loyal"] > 3 and npc["relation_player"] > 4:
        return "assist_player"

    if npc["goal"] == "gain_gold":
        return random.choice(["travel", "fight", "trade"])

    if npc["goal"] == "explore":
        return "travel"

    if npc["goal"] == "revenge":
        return "fight"

    return random.choice(["travel", "rest"])


def resolve_npc_action(npc, action, game_state):
    npc_behavior(npc)
    
    if action == "travel":
        npc["location"] = random.choice(
            ["route", "village", "ruines"]
        )

        print(f"{npc['name']} va à {npc['location']}.")
    elif action == "fight":
        npc["goal"] = "revenge"

        if random.random() < 0.3:
            npc["hp"] -= 3
            print(f"{npc['name']} a été blessé.")

            if npc["hp"] <= 0:
                npc["alive"] = False

                m.add_memory(
                    game_state,
                    "npc_killed",
                    f"{npc['name']} a été tué.",
                    ["player", npc["name"]],
                    importance=3
                )

                print(f"{npc['name']} est mort hors écran.")
    elif action == "trade":
        npc["gold"] += 2

        print(f"{npc['name']} fait du commerce et gagne 2 pièces.")
    elif action == "assist_player":
        print(f"{npc['name']} cherche à te rendre la faveur.")
    else:
        print(f"{npc['name']} se repose.")


def react_to_world_event(npc, event):
    if event["type"] == "npc_killed":
        if event["npc"] in npc["relationships"]:
            relation = npc["relationships"][event["npc"]]
    
            if relation > 40:
                npc["emotions"]["sadness"] += 30
                npc["emotions"]["anger"] += 10
    
            elif relation < -40:
                npc["emotions"]["joy"] += 10


def get_dominant_emotion(npc):
    return max(npc["emotions"], key=npc["emotions"].get)


def npc_behavior(npc):
    emotion = get_dominant_emotion(npc)
    
    if emotion == "anger":
        print(npc["name"], "agit agressivement")
    elif emotion == "fear":
        print(npc["name"], "évite les dangers")
    elif emotion == "joy":
        print(npc["name"], "est amical")
    elif emotion == "sadness":
        print(npc["name"], "reste isolé")


def decay_emotions(npc):
    for emotion in npc["emotions"]:
        npc["emotions"][emotion] *= 0.9