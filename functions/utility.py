import streamlit as st
from streamlit_extras.let_it_rain import rain
from typing import Tuple, Dict, List, Union
from icecream import ic
import yaml
import json
from functions import redis_functions
import random


def read_yaml(file_path) -> Union[Dict, List]:
    """Read the specified file and return as a dictionary or list."""
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_app_config(config_name=None):
    path = "config_riddle_of_the_ring.yaml"
    app_config = read_yaml(path)
    if config_name:
        return app_config[config_name]
    return app_config


def initialize_game_data(data=None, game_code: str = None, *, category: str):
    if data is None:
        with open(f"data/{category}.yaml") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    redis_functions.set_data(category, json.dumps(data), game_code=game_code)


def validate_game_data():
    """Validate game data is set and, if not, set it."""
    keys = ["characters", "games"]
    game_datas = [{"key": "characters"}, {"key": "games", "data": []}]
    for game_data in game_datas:
        key = game_data.get("key")
        data = game_data.get("data")
        if not redis_functions.data_exists(key):
            print(f"++++initializing game data | key={key}++++")
            initialize_game_data(category=key, data=data)
    return


def check_time_exceeded(viewing_time):
    is_time_exceeded = False
    if st.session_state["is_auto_refresh"]:
        auto_refresh_interval = st.session_state["auto_refresh_interval"]
        max_view_counter = viewing_time / auto_refresh_interval
        if "view_counter" not in st.session_state:
            st.session_state["view_counter"] = 0
        st.session_state["view_counter"] += 1
        if st.session_state["view_counter"] >= max_view_counter:
            is_time_exceeded = True
            del st.session_state["view_counter"]
    else:
        is_time_exceeded = True
    return is_time_exceeded


def get_data(category: str, game_code=None):
    data = redis_functions.get_data(category, game_code=game_code)
    # print("get_data", category, data)
    if data is not None:
        return json.loads(data)
    return data
    # with open(f"data/{category}.yaml") as f:
    #     data = yaml.load(f, Loader=yaml.SafeLoader)
    # return data


def set_data(category: str, data, game_code=None):
    redis_functions.set_data(category, json.dumps(data), game_code=game_code)


def get_item(category: str, id: int, game_code=None):
    items = get_data(category, game_code=game_code)
    for item in items:
        if item["id"] == id:
            return item
    return None


def add_activity(action, type="system"):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    player = players[player_code]
    activities = get_data("activities", game_code=game_code)
    activity = {
        "player": {"character": player["character"]},
        "action": action,
        "type": type,
    }
    activities.append(activity)
    set_data("activities", activities, game_code=game_code)


# @st.cache_data
def get_cards():
    cards = read_yaml("data/cards.yaml")
    return cards


def get_card_owner(card_id):
    game_code = st.query_params.game
    players = get_data("players", game_code=game_code)
    for player in players.values():
        if card_id in player["cards"]:
            return player
    return None


def get_card(card_id):
    cards = get_cards()
    for card in cards:
        if card["id"] == card_id:
            return card
    return None


def get_player(character):
    game_code = st.query_params.game
    players = get_data("players", game_code=game_code)
    for player in players.values():
        if player["character"] == character:
            return player
    return None


def get_shuffled_deck():
    cards = get_cards()
    cards = [
        card["id"] for card in cards if card.get("include_in_draw_pile") is not False
    ]
    print(cards)
    random.shuffle(cards)
    return cards


def reset_draw_pile():
    game_code = st.query_params.game
    new_draw_pile = get_data("discards", game_code=game_code)
    random.shuffle(new_draw_pile)
    random.shuffle(new_draw_pile)
    set_data("draw_pile", new_draw_pile, game_code=game_code)
    set_data("discards", [], game_code=game_code)
    add_activity("Resetting the draw pile!")
    return


def get_player_cards(player_id: int = None, character: str = None):
    game_code = st.query_params.game
    if player_id is not None:
        player = get_item("players", player_id, game_code=game_code)
        if player:
            return player["cards"]
        return None
    elif character:
        players = get_data("players", game_code=game_code)
        for player in players:
            if player["character"] == character:
                return player["cards"]
        return None


def shuffle_player_cards():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    player_cards = players[player_code]["cards"]
    random.shuffle(player_cards)
    players[player_code]["cards"] = player_cards
    set_data("players", players, game_code=game_code)
    return


def add_selected_card(card_id, selected_card_index=None, card_owner_player_code=None):
    game_code = st.query_params.game
    player_code = st.query_params.player
    unselect_all_cards()
    players = get_data("players", game_code=game_code)
    if card_owner_player_code != player_code:
        card_owner_cards = players[card_owner_player_code]["cards"]
        card_id = card_owner_cards[selected_card_index]
    players[player_code]["selected_cards"].append(card_id)
    set_data("players", players, game_code=game_code)
    return


def unselect_card(card_id, for_all_players: bool = None):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    is_updated = False
    if for_all_players:
        for player in players.values():
            if card_id in player["selected_cards"]:
                player["selected_cards"].remove(card_id)
                is_updated = True

    else:
        if card_id in players[player_code]["selected_cards"]:
            players[player_code]["selected_cards"].remove(card_id)
            is_updated = True
    if is_updated:
        set_data("players", players, game_code=game_code)
    return


def unselect_all_cards():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    selected_cards = players[player_code]["selected_cards"].copy()
    for card_id in selected_cards:
        unselect_card(card_id)


# def add_in_use_card(card_id):
#     unselect_card(card_id=card_id)
#     st.session_state["in_use_cards"].append(card_id)


def is_card_selected(card_id):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    if card_id in players[player_code]["selected_cards"]:
        return True
    else:
        return False


# def is_card_in_use(card_id):
#     if card_id in st.session_state["in_use_cards"]:
#         return True
#     else:
#         return False


def is_card_selected_or_in_use(card_id):
    is_selected = is_card_selected(card_id=card_id)
    # is_in_use = is_card_in_use(card_id=card_id)
    # return any([is_selected, is_in_use])
    return is_selected


def draw_cards(number=1, player_code=None):
    game_code = st.query_params.game
    if player_code is None:
        player_code = st.query_params.player
    draw_pile = get_data("draw_pile", game_code=game_code)
    if number > len(draw_pile):
        reset_draw_pile()
        draw_pile = get_data("draw_pile", game_code=game_code)
    draw_cards = []
    for x in range(number):
        draw_cards.append(draw_pile.pop())
    set_data("draw_pile", draw_pile, game_code=game_code)
    players = get_data("players", game_code=game_code)
    players[player_code]["cards"].extend(draw_cards)
    # for player in players:
    #     if player["id"] == this_player["id"]:
    #         player["cards"].extend(draw_cards)
    set_data("players", players, game_code=game_code)
    return draw_cards


def update_players(players):
    game_code = st.query_params.game
    set_data("players", players, game_code=game_code)


def add_card_to_hand(card_id, character=None):
    game_code = st.query_params.game
    if character:
        player = get_player(character)
        player_code = player["player_code"]
    else:
        player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    if card_id not in players[player_code]["cards"]:
        players[player_code]["cards"].append(card_id)
        set_data("players", players, game_code=game_code)
    return


def remove_card_from_hand(card_id, player_code=None):
    game_code = st.query_params.game
    if player_code is None:
        player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    if card_id in players[player_code]["cards"]:
        players[player_code]["cards"].remove(card_id)
        set_data("players", players, game_code=game_code)
    return


def add_card_to_discard(card_id):
    card = get_card(card_id)
    is_discardable = card.get("is_discardable", True)
    if is_discardable:
        game_code = st.query_params.game
        unselect_card(card_id, for_all_players=True)
        discards = get_data("discards", game_code=game_code)
        if card_id not in discards:
            discards.append(card_id)
            set_data("discards", discards, game_code=game_code)
            remove_card_from_hand(card_id)
            remove_table_card(card_id)
            add_activity(f"Discard ({card['name']})")


def keep_card(card_id):
    if card_id in st.session_state["in_use_cards"]:
        st.session_state["in_use_cards"].remove(card_id)
    print(f"keeping card {card_id}")


def use_card_for_battle(card_id, battle_role):
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    if card_id not in battle[f"{battle_role}_cards"]:
        battle[f"{battle_role}_cards"].append(card_id)
    set_data("battle", battle, game_code=game_code)
    return


def remove_battle_card(card_id, battle_role):
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    if card_id in battle[f"{battle_role}_cards"]:
        battle[f"{battle_role}_cards"].remove(card_id)
        set_data("battle", battle, game_code=game_code)
    return


def discard_battle_card(card_id, battle_role):
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    if card_id in battle[f"{battle_role}_cards"]:
        battle[f"{battle_role}_cards"].remove(card_id)
        set_data("battle", battle, game_code=game_code)
    add_card_to_discard(card_id)
    return


def retain_battle_card(card_id, battle_role):
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    if card_id in battle[f"{battle_role}_cards"]:
        battle[f"{battle_role}_cards"].remove(card_id)
        set_data("battle", battle, game_code=game_code)
    return


def add_city_battle_card(battle_role, side):
    if side == "good":
        card_id = 91
    if side == "evil":
        card_id = 92
    use_card_for_battle(card_id, battle_role)


def transfer_card(card_id, character=None):
    card_owner = get_card_owner(card_id)
    remove_card_from_hand(card_id, card_owner["player_code"])
    add_card_to_hand(card_id, character=character)
    unselect_card(card_id)
    return


def place_card_on_table(card_id):
    game_code = st.query_params.game
    table_cards = get_data("table_cards", game_code=game_code)
    table_cards.append(card_id)
    set_data("table_cards", table_cards, game_code=game_code)


def remove_table_card(card_id):
    game_code = st.query_params.game
    table_cards = get_data("table_cards", game_code=game_code)
    if card_id in table_cards:
        table_cards.remove(card_id)
        set_data("table_cards", table_cards, game_code=game_code)
    return


def show_hand_to_character():
    character = st.session_state["show_hand_to_character"]
    st.session_state.pop("show_hand_to_character")
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    players[player_code]["special_actions"]["show_hand_to_character"] = character
    set_data("players", players, game_code=game_code)
    action = "Show Hand to Player"
    add_activity(f"{action} ({character})")
    return


def show_card_to_character(card_id):
    character = st.session_state["show_card_to_character"]
    st.session_state.pop("show_card_to_character")
    game_code = st.query_params.game
    show_card_to_player = {"show_card_to_character": character, "show_card": card_id}
    set_data("show_card_to_player", show_card_to_player, game_code=game_code)
    action = "Show Card to Player"
    add_activity(f"{action} ({character})")
    return


def give_card_to_character(card_id):
    character = st.session_state["give_card_to_character"]
    st.session_state.pop("give_card_to_character")
    transfer_card(card_id, character=character)
    action = "Give Card to Player"
    add_activity(f"{action} ({character})")
    return


def riddle_player(card_id):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    this_character = players[player_code]["character"]
    card_owner = get_card_owner(card_id)
    character = card_owner["character"]
    riddle_power_play = {
        "riddle_card": card_id,
        "card_owner": character,
        "riddler": this_character,
        "can_riddler_see_card": False,
    }
    set_data("riddle_power_play", riddle_power_play, game_code=game_code)
    action = "Riddle Player"
    add_activity(f"{action} ({character})")
    return


def use_card_in_friendly_exchange(card_id):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    this_character = players[player_code]["character"]
    card_owner = get_card_owner(card_id)
    character = card_owner["character"]
    friendly_exchange = get_data("friendly_exchange", game_code=game_code)
    if friendly_exchange:
        first_party = friendly_exchange["first_party"]
        second_party = friendly_exchange["second_party"]
        is_first_party = character == first_party
        is_second_party = this_character == second_party
        if not is_first_party:
            st.error(f"Pick a card belonging to {first_party}")
        if not is_second_party:
            st.error(
                f"Only {first_party} and {second_party} can participate in this friendly exchange"
            )
        if is_second_party:
            friendly_exchange[this_character] = {
                "character": character,
                "card": card_id,
            }
            friendly_exchange["status"] = "ready"
    else:
        friendly_exchange = {
            this_character: {"character": character, "card": card_id},
            "status": "pending",
            "first_party": this_character,
            "second_party": character,
        }
    set_data("friendly_exchange", friendly_exchange, game_code=game_code)
    action = "Friendly Exchange"
    add_activity(f"{action} ({character})")
    return


@st.cache_data
def get_emojis():
    emojis = {"cats": "🐈", "dogs": "🌭", "balloons": "🎈"}
    return emojis


def let_it_rain(emoji="🎈", key=None):
    if key is not None:
        emoji = get_emojis().get(key)
    if emoji:
        rain(
            emoji=emoji,
            font_size=54,
            falling_speed=5,
            animation_length="infinite",
        )


def set_next_turn():
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    turn_order: List = list(players.keys())
    current_turn_index = turn_order.index(player_code)
    num_players = len(players)
    next_turn_index = current_turn_index + 1
    next_turn_index = next_turn_index % num_players
    next_player_code = turn_order[next_turn_index]
    players[player_code]["current_turn"] = False
    players[next_player_code]["current_turn"] = True
    set_data("players", players, game_code=game_code)
    return


def start_game():
    game_code = st.query_params.game
    game = get_data("game", game_code=game_code)
    if game["is_started"] == False:
        game["is_started"] = True
        set_data("game", game, game_code=game_code)
        players = get_data("players", game_code=game_code)
        player_codes = list(players.keys())
        player_code = random.choice(player_codes)
        players[player_code]["current_turn"] = True
        set_data("players", players, game_code=game_code)
        for player_code in player_codes:
            draw_cards(number=2, player_code=player_code)
    return


def add_game_stat(key, value):
    game_code = st.query_params.game
    game = get_data("game", game_code=game_code)
    game["stats"][key] = value
    set_data("game", game, game_code=game_code)
    return


def add_game_metric(name, key, type="incrementer"):
    game_code = st.query_params.game
    game = get_data("game", game_code=game_code)
    game["metrics"][name][str(key)] += 1
    set_data("game", game, game_code=game_code)
    return


def set_action(action, card_id):
    card = get_card(card_id)
    # action = st.session_state[f"action_{card_id}"]
    # st.session_state[f"action_{card_id}"] = None
    if action == "Unselect":
        unselect_card(card_id)
        return
    elif action == "Use to Defend":
        use_card_for_battle(card_id, "defender")
    elif action == "Use to Attack":
        use_card_for_battle(card_id, "attacker")
    elif action == "Discard":
        add_card_to_discard(card_id)
        return
    elif action == "Take Card from Player":
        card_owner = get_card_owner(card_id)
        transfer_card(card_id)
        add_activity(f"{action} (from {card_owner['character']})")
        return
    elif action == "Place on Table":
        place_card_on_table(card_id)
    elif action == "Take Card in Friendly Exchange":
        use_card_in_friendly_exchange(card_id)
        return
    elif action == "Riddle Player":
        riddle_player(card_id)
        return
    elif action == "Show Card to Player":
        st.session_state["show_card_to_character"] = True
        return
    elif action == "Give Card to Player":
        st.session_state["give_card_to_character"] = True
        return
    add_activity(f"{action} ({card['name']})")
    return


def set_general_action(action=None):
    if action is None:
        action = st.session_state[f"general_action"]
        st.session_state[f"general_action"] = None
    if action == "Attack from Good City":
        add_city_battle_card("attacker", "good")
    elif action == "Attack from Evil City":
        add_city_battle_card("attacker", "evil")
    elif action == "Defend from Good City":
        add_city_battle_card("defender", "good")
    elif action == "Defend from Evil City":
        add_city_battle_card("defender", "evil")
    elif action == "Show Hand to Player":
        st.session_state["show_hand_to_character"] = True
        return
    elif action == "Draw Card":
        draw_cards(1)
    elif action == "Roll Die":
        roll = random.randint(1, 6)
        add_game_stat("Last Roll", roll)
        add_game_metric("Rolls", roll)
        action += f": {roll}"
    elif action == "End Turn":
        set_next_turn()
    elif action == "Start Game":
        start_game()
    add_activity(action)


def show_battle_section():
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    battle_roles = ["attacker", "defender"]
    for battle_role in battle_roles:
        if battle[f"{battle_role}_cards"]:
            return True
    return False
