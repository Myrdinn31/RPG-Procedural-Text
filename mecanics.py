import random

import fight as f
import event as e
import dungeon as d


def roll_d20():
    return random.randint(1, 20)


def test(stat, difficulty):
    roll = roll_d20()
    total = roll + stat
    
    return total >= difficulty, roll, total


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
                    importance=2
                )
            else:
                damage_player(player, 3, game_state)

                add_memory(
                    game_state,
                    "bandit_negociation",
                    "La négociation avec le bandit n'a pas fonctionné.",
                    ["player", "bandit"],
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
            importance=2
        )
    elif choice["type"] == "hear_rumor":
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
            importance=1
        )


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


def add_memory(game_state, memory_type, text, actors, importance=1):
    memory = {
        "day": game_state["day"],
        "type": memory_type,
        "text": text,
        "actors": actors,
        "importance": importance
    }

    game_state["history"].append(memory)


def summarize_history(game_state):
    print("\n=== Chroniques du Monde ===")

    # for memory in game_state["history"][-5:]:
    for memory in game_state["history"]:
        print(f"Jour {memory['day']} — {memory['text']}")


def travel_player(game_state):
    current = game_state["player"]["location"]
    neighbors = game_state["locations"][current]["neighbors"]

    print("Où veux-tu aller ?")

    for i, loc in enumerate(neighbors):
        print(f"{i+1}. {loc}")

    choice = int(input("> ")) - 1
    game_state["player"]["location"] = neighbors[choice]