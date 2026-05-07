def create_quest(qtype, description, target=None, location=None, npc=None, faction=None):
    return {
        "type": qtype,
        "description": description,
        "target": target,
        "location": location,
        "status": "active",
        "progress": 0,
        "giver": npc,
        "faction": faction
    }


def generate_quests_from_memory(game_state):
    quest = None
    
    for memory in game_state["history"]:
        # éviter duplication
        if memory.get("used_for_quest"):
            continue

        if memory["type"] == "npc_killed":
            quest = create_quest(
                "investigate",
                f"Enquêter sur la mort de {memory['actors'][1]}",
                target=memory["actors"][1],
                location=memory["location"]
            )
        elif memory["type"] == "bandits_active":
            quest = create_quest(
                "protect",
                "Sécuriser la route contre les bandits",
                location=memory["location"]
            )
        elif memory["type"] == "location_discovered":
            quest = create_quest(
                "explore",
                f"Explorer {memory['location']}",
                location=memory["location"]
            )

        if quest:
            game_state["quests"].append(quest)
            memory["used_for_quest"] = True


def update_quests(game_state):
    for quest in game_state["quests"]:
        if quest["status"] != "active":
            continue

        # exemple : aller à un lieu
        if quest["type"] == "explore":
            if game_state["player"]["location"] == quest["location"]:
                quest["status"] = "completed"
                print("Quête accomplie !")

                complete_quest(game_state, quest)


def complete_quest(game_state, quest):
    print("Quête terminée :", quest["description"])

    game_state["player"]["gold"] += 10
    quest["status"] = "done"