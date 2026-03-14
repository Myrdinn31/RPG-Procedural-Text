import random

import mecanics as m
import npc as n


def combat(player, enemy, game_state):
    print(f"Combat contre {enemy['name']} !")

    while enemy["hp"] > 0 and player["hp"] > 0:
        input("Appuie sur Entrée pour attaquer...")

        player_roll = random.randint(1,20)
        enemy_roll = random.randint(1,20)
        player_total = player_roll + player["strength"]
        enemy_total = enemy_roll + enemy["attack"]

        if player_total >= enemy_total:
            print(f"Tu réussis ton jet : {player_roll} + {player['strength']} ({player_total}) contre {enemy_roll} + {enemy['attack']} ({enemy_total})")
            
            dmg = random.randint(2,5)
            enemy["hp"] -= dmg
            print(f"Tu infliges {dmg} dégâts.")
        else:
            print(f"Tu rates ton jet : {player_roll} + {player['strength']} ({player_total}) contre {enemy_roll} + {enemy['attack']} ({enemy_total})")
            
            dmg = random.randint(1,4)
            m.damage_player(player, dmg, game_state)

        print(f"HP Joueur: {player['hp']} | HP Ennemi: {enemy['hp']}")

    if player["hp"] > 0:
        print("Victoire !")
    
        m.add_memory(
            game_state,
            "fight_win",
            f"Le joueur a tué {enemy['name']}.",
            ["player", {enemy['name']}],
            importance=3
        )
    else:
        print("Défaite...")
    
        m.add_memory(
            game_state,
            "fight_lose",
            f"{enemy['name']} a tué le joueur.",
            ["player", {enemy['name']}],
            importance=3
        )

    if player["hp"] > 0:
        if enemy['faction'] == "bandits":
            n.change_reputation(game_state, "bandits", -2)
            n.change_reputation(game_state, "royaume", +1)
        
            ''' for other, relation in n.faction_relations.get("bandits", {}).items():
                n.change_reputation(game_state, other, int(-2 * relation / 10))
        
            for other, relation in n.faction_relations.get("royaume", {}).items():
                n.change_reputation(game_state, other, int(1 * relation / 10)) '''
        elif enemy['faction'] == "royaume":
            n.change_reputation(game_state, "bandits", +2)
            n.change_reputation(game_state, "mage", -1)
            n.change_reputation(game_state, "royaume", -2)

            ''' for other, relation in n.faction_relations.get("bandits", {}).items():
                n.change_reputation(game_state, other, int(+2 * relation / 10))

            for other, relation in n.faction_relations.get("mage", {}).items():
                n.change_reputation(game_state, other, int(-1 * relation / 10))

            for other, relation in n.faction_relations.get("royaume", {}).items():
                n.change_reputation(game_state, other, int(-2 * relation / 10)) '''
        elif enemy['faction'] == "mage":
            n.change_reputation(game_state, "mage", -2)
            n.change_reputation(game_state, "royaume", -1)

            ''' for other, relation in n.faction_relations.get("mage", {}).items():
                n.change_reputation(game_state, other, int(-2 * relation / 10))

            for other, relation in n.faction_relations.get("royaume", {}).items():
                n.change_reputation(game_state, other, int(-1 * relation / 10)) '''