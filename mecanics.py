import random

import fight as f
import event as e
import dungeon as d
import npc as n
import quest as q


LIKELIHOODS = {
    "impossible": 10,
    "nearly_impossible": 15,
    "very_unlikely": 25,
    "unlikely": 35,
    "50_50": 50,
    "likely": 65,
    "very_likely": 75,
    "nearly_certain": 85,
    "certain": 90
}


def roll_d20():
    return random.randint(1, 20)


def test(stat, difficulty):
    roll = roll_d20()
    total = roll + stat
    
    return total >= difficulty, roll, total


def adjust_chance(base_chance, chaos_factor):
    return base_chance + (chaos_factor - 5) * 5


def fate_check(game_state, likelihood):
    chaos = game_state["chaos_factor"]
    base = LIKELIHOODS[likelihood]

    # ajustement
    chance = adjust_chance(base, chaos)

    # clamp (important)
    chance = max(1, min(99, chance))

    roll = random.randint(1, 100)

    # seuils
    exceptional_yes_threshold = max(1, int(chance * 0.2))
    exceptional_no_threshold = min(100, 100 - int((100 - chance) * 0.2))

    if roll >= 10:
        if str(roll)[0] == str(roll)[1]:  # ex: 11, 22, 33...
            if roll <= chaos * 11:
                # trigger_random_event()
                print("Un événement chaotique se produit !")

    if roll <= exceptional_yes_threshold:
        return "exceptional_yes", roll
    elif roll <= chance:
        return "yes", roll
    elif roll >= exceptional_no_threshold:
        return "exceptional_no", roll
    else:
        return "no", roll
    

def interpret_result(result):
    if result == "exceptional_yes":
        return "Oui, et c’est encore plus intense que prévu."
    if result == "yes":
        return "Oui."
    if result == "no":
        return "Non."
    if result == "exceptional_no":
        return "Non, et quelque chose d’inattendu se produit."


def resolve_choice(game_state, event, choice):
    player = game_state["player"]
    location = player["location"]
    danger = game_state["locations"][location]["danger"]

    if choice["type"] == "combat":
        f.combat(player, {
            "name": "Bandit",
            "hp": 5 + danger * 2,
            "attack": 2,
            "faction": "bandits"
        }, game_state)
    elif choice["type"] == "test":
        success, roll, total = test(
            player[choice["stat"]],
            choice["difficulty"]
        )

        if event == e.event_bandit:
            print(f"{roll} + {player[choice['stat']]} ({total}) contre {choice['difficulty']}")
            
            if success:
                print("Le bandit te laisse passer.")

                add_memory(
                    game_state,
                    "bandit_negociation",
                    "La négociation avec le bandit a fonctionné.",
                    ["player", "bandit"],
                    game_state["player"]["location"],
                    register_witnesses(game_state, game_state["player"]["location"]),
                    importance=2
                )
            else:
                damage_player(player, 3, game_state)

                add_memory(
                    game_state,
                    "bandit_negociation",
                    "La négociation avec le bandit n'a pas fonctionné.",
                    ["player", "bandit"],
                    game_state["player"]["location"],
                    register_witnesses(game_state, game_state["player"]["location"]),
                    importance=2
                )
        elif event == e.event_traveler:
            print(f"{roll} + {player[choice['stat']]} ({total}) contre {choice['difficulty']}")

            if success:
                heal_player(player, 3, game_state)
                print("Ce que tu manges te soigne.")

                add_memory(
                    game_state,
                    "campfire_heal",
                    "Le joueur a récupéré de la santé en mangeant au coin du feu.",
                    ["player", "npc"],
                    game_state["player"]["location"],
                    register_witnesses(game_state, game_state["player"]["location"]),
                    importance=2
                )
            else:
                damage_player(player, 3, game_state)
                print("Ce que tu manges te rend malade.")

                add_memory(
                    game_state,
                    "campfire_damage",
                    "Le joueur a perdu de la santé en mangeant au coin du feu.",
                    ["player", "npc"],
                    game_state["player"]["location"],
                    register_witnesses(game_state, game_state["player"]["location"]),
                    importance=2
                )
    elif choice["type"] == "continuer":
        if event == e.event_traveler:
            print("Tu continues ton chemin.")

            add_memory(
                game_state,
                "campfire",
                "Tu as rencontré un NPC au coin du feu mais tu as continué ton chemin.",
                ["player", "npc"],
                game_state["player"]["location"],
                register_witnesses(game_state, game_state["player"]["location"]),
                importance=1
            )
    elif choice["type"] == "enter_dungeon":
        game_state["dungeon"] = d.generate_dungeon(random.randint(1, 10))
        d.explore_dungeon(game_state)
    elif choice["type"] == "talk_npc":
        npc = event["npc"]
        npc["relation_player"] += 1
        npc["last_seen_day"] = game_state["day"]
        
        print(f"Tu discutes avec {npc['name']}.")

        add_memory(
            game_state,
            "npc_talk",
            f"Tu as discuté avec {npc['name']}.",
            ["player", npc["name"]],
            game_state["player"]["location"],
            register_witnesses(game_state, game_state["player"]["location"]),
            importance=1
        )
    elif choice["type"] == "combat_npc":
        npc = event["npc"]
        
        f.combat(game_state["player"], {
            "name": npc["name"],
            "hp": npc["hp"] + danger * 2,
            "attack": 2,
            "faction": npc["faction"]
        }, game_state)

        npc["last_seen_day"] = game_state["day"]
        npc["alive"] = False
    elif choice["type"] == "help_npc":
        npc = event["npc"]
        
        print(f"Tu aides {npc['name']}.")
        
        # amélioration relation
        npc["relation_player"] += 3
        
        # mémoire individuelle du PNJ
        npc["memories"].append({
            "type": "helped_by_player",
            "day": game_state["day"]
        })

        # mémoire globale du monde
        add_memory(
            game_state,
            "npc_helped",
            f"Le joueur a aidé {npc['name']}.",
            ["player", npc["name"]],
            game_state["player"]["location"],
            register_witnesses(game_state, game_state["player"]["location"]),
            importance=2
        )
    elif choice["type"] == "hear_rumor_player":
        important_memories = [
            m for m in game_state["history"]
            if m["importance"] >= 2
        ]

        memory = random.choice(important_memories)
        print(f"Rumeur : {memory['text']}")

        add_memory(
            game_state,
            "rumor",
            "Le joueur a entendu une rumeur.",
            ["player"],
            game_state["player"]["location"],
            register_witnesses(game_state, game_state["player"]["location"]),
            importance=1
        )
    elif choice["type"] == "hear_rumor":
        rumors = [
            m for m in game_state["history"]
            if game_state["player"]["location"] == m["location"]
            or game_state["player"]["name"] in m["known_by"]
        ]

        if rumors:
            rumor = random.choice(rumors)
            print(f"Rumeur : {rumor['text']}")
    elif choice["type"] == "show_quests":
        for i, q in enumerate(game_state["quests"]):
            print(f"{i+1}. {q['description']}")
    elif choice["type"] == "combat_advantage":
        start_combat(advantage=True)
    elif choice["type"] == "gain_ally":
        add_companion(choice["npc"])


def damage_player(player, amount, game_state):
    player["hp"] -= amount
    print(f"Tu perds {amount} HP.")

    if player["hp"] <= 0:
        print("Tu es mort...")
        summarize_history(game_state)
        exit()


def heal_player(player, amount, game_state):
    player["hp"] += amount
    print(f"Tu gagnes {amount} HP.")
    
    if player["hp"] <= 0:
        print("Tu es mort...")
        summarize_history(game_state)
        exit()


def add_memory(game_state, memory_type, text, actors, location, known_by, importance=1):
    memory = {
        "day": game_state["day"],
        "type": memory_type,
        "text": text,
        "actors": actors,
        "location": location,
        "importance": importance,
        "known_by": known_by,
        "spread_level": 0
    }

    game_state["history"].append(memory)

    q.generate_quests_from_memory(game_state)


def summarize_history(game_state):
    print("\n=== Chroniques du Monde ===")

    # for memory in game_state["history"][-5:]:
    for memory in game_state["history"]:
        print(f"Jour {memory['day']} — {memory['text']}")


def world_status(game_state):
    print("\n\n=== Statut du Monde ===")

    print(f"Joueur => Nom : {game_state['player']['name']} / HP : {game_state['player']['hp']} / Argent : {game_state['player']['gold']} / Statut : {', '.join(game_state['player']['status'])} / Lieu : {game_state['player']['location']}")
    print(f"Jour : {game_state['day']} / Danger : {game_state['world']['danger_level']} / Guerre : {game_state['world']['war']} / Bandits actifs : {game_state['world']['bandits_active']} / Économie : {game_state['world']['economy']}")
    print(f"Donjon : {', '.join(game_state['dungeon'])}")
    print(f"Factions => Royaume : {game_state['factions']['royaume']['reputation']} / Bandits : {game_state['factions']['bandits']['reputation']} / Mages : {game_state['factions']['mages']['reputation']}")


def travel_player(game_state):
    current = game_state["player"]["location"]
    neighbors = game_state["locations"][current]["neighbors"]

    print("Où veux-tu aller ?")

    for i, loc in enumerate(neighbors):
        print(f"{i+1}. {loc}")

    choice = int(input("> ")) - 1
    game_state["player"]["location"] = neighbors[choice]


def register_witnesses(game_state, location):
    known_by = []

    for npc in game_state["npcs"]:
        if npc["location"] == location and npc["alive"]:
            known_by.append(npc["name"])

    return known_by


def spread_rumors(game_state):
    for memory in game_state["history"]:
        for npc in game_state["npcs"]:
            if not npc["alive"]:
                continue
            # si PNJ connaît la rumeur
            if npc["name"] in memory["known_by"]:
                # transmettre à d'autres PNJ au même endroit
                for other in game_state["npcs"]:
                    if other["name"] == npc["name"]:
                        continue
                    if other["location"] == npc["location"]:
                        chance = 0.3 + (memory["importance"] * 0.1) + (memory["spread_level"] * 0.05)

                        if random.random() < chance:
                            memory["known_by"].append(other["name"])

                            memory["spread_level"] += 1

                            n.npc_react_to_rumors(npc, memory)