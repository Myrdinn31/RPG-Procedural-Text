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

    npc_social_phase(game_state)


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
        move_npc(npc, game_state);

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


def move_npc(npc, game_state):
    current = npc["location"]
    neighbors = game_state["locations"][current]["neighbors"]
    
    npc["location"] = random.choice(neighbors)


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


def generate_npc_choices(npc):
    choices = []

    relation = npc["relation_player"]
    traits = npc["traits"]
    emotions = npc["emotions"]

    # PNJ agressif
    if traits["aggressive"] > 4 or emotions["anger"] > 50:
        choices.append({"text": "Se défendre", "type": "combat_npc"})
        return choices

    # PNJ ami
    if relation > 5:
        choices.append({"text": "Discuter", "type": "talk_npc"})
        choices.append({"text": "Demander de l'aide", "type": "ask_help"})
        choices.append({"text": "Voyager ensemble", "type": "recruit_npc"})
    # PNJ neutre
    elif -3 <= relation <= 5:
        choices.append({"text": "Discuter", "type": "talk_npc"})
        choices.append({"text": "Aider", "type": "help_npc"})
    # PNJ hostile
    else:
        choices.append({"text": "Tenter d'apaiser", "type": "calm_npc"})
        choices.append({"text": "Combattre", "type": "combat_npc"})
    # PNJ cupide
    if traits["greedy"] > 3:
        choices.append({"text": "Offrir de l'or", "type": "bribe_npc"})

    return choices


def npc_social_phase(game_state):
    npcs = game_state["npcs"]

    for i in range(len(npcs)):
        for j in range(i + 1, len(npcs)):
            npc_a = npcs[i]
            npc_b = npcs[j]

            if not npc_a["alive"] or not npc_b["alive"]:
                continue

            if npc_a["location"] == npc_b["location"]:
                if random.random() < 0.25:
                    npc_interaction(npc_a, npc_b)


def npc_interaction(npc_a, npc_b):
    print(f"{npc_a['name']} rencontre {npc_b['name']}.")

    relation = npc_a["relationships"].get(npc_b["name"], 0)

    # traits
    aggressive = npc_a["traits"]["aggressive"]
    greedy = npc_a["traits"]["greedy"]

    # combat
    if aggressive > 4 and random.random() < 0.4:
        print("Une bagarre éclate.")
        npc_b["hp"] -= 3
        relation -= 3
    # commerce
    elif greedy > 3 and random.random() < 0.4:
        print("Ils échangent des marchandises.")
        relation += 1
    # discussion
    else:
        print("Ils discutent tranquillement.")
        relation += 1

    if npc_a["emotions"]["anger"] > 40:
        relation -= 2
    if npc_a["emotions"]["joy"] > 40:
        relation += 2

    npc_a["relationships"][npc_b["name"]] = relation
    npc_b["relationships"][npc_a["name"]] = relation

    print(f"La relation évolue entre {npc_a['name']} et {npc_b['name']} : {relation}.")