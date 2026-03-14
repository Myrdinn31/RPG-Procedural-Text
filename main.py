import world as w
import npc as n
import event as e


def main():
    w.game_state["npcs"].append(n.create_npc("Roderic"))
    w.game_state["npcs"].append(n.create_npc("Elena"))

    while True:
        all_events = e.get_all_events(w.game_state)
        event = e.choose_event(w.game_state, all_events)
        e.play_event(w.game_state, event)

        w.update_world(w.game_state)
        w.game_state["day"] += 1
        print(f"\nJour {w.game_state['day']}")


if __name__ == "__main__":
    main()