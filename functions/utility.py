import streamlit as st
from typing import Tuple, Dict, List, Union
from icecream import ic
import yaml
import json
from models import Player
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


def add_activity(action):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    player = players[player_code]
    activities = get_data("activities", game_code=game_code)
    activity = {"player": {"character": player["character"]}, "action": action}
    activities.append(activity)
    set_data("activities", activities, game_code=game_code)


@st.cache_data
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


def get_shuffled_deck():
    cards = get_cards()
    cards = [
        card["id"] for card in cards if card.get("include_in_draw_pile") is not False
    ]
    print(cards)
    random.shuffle(cards)
    return cards


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


def add_selected_card(card_id):
    game_code = st.query_params.game
    player_code = st.query_params.player
    players = get_data("players", game_code=game_code)
    player = players[player_code]
    ic(player)
    # st.session_state["selected_cards"].append(card_id)
    players[player_code]["selected_cards"].append(card_id)
    set_data("players", players, game_code=game_code)


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


def draw_cards(number=1):
    game_code = st.query_params.game
    player_code = st.query_params.player
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


def add_card_to_hand(card_id):
    game_code = st.query_params.game
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
    game_code = st.query_params.game
    unselect_card(card_id, for_all_players=True)
    discards = get_data("discards", game_code=game_code)
    discards.append(card_id)
    set_data("discards", discards, game_code=game_code)
    remove_card_from_hand(card_id)
    add_activity(f"Discard ({card['name']})")


def keep_card(card_id):
    if card_id in st.session_state["in_use_cards"]:
        st.session_state["in_use_cards"].remove(card_id)
    print(f"keeping card {card_id}")


def use_card_for_battle(card_id, battle_role):
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
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
        card_id = 24
    if side == "evil":
        card_id = 25
    use_card_for_battle(card_id, battle_role)


def transfer_card(card_id):
    card_owner = get_card_owner(card_id)
    remove_card_from_hand(card_id, card_owner["player_code"])
    add_card_to_hand(card_id)
    unselect_card(card_id)
    return


def place_card_on_table(card_id):
    game_code = st.query_params.game
    table_cards = get_data("table_cards", game_code=game_code)
    table_cards.append(card_id)
    set_data("table_cards", table_cards, game_code=game_code)


def discard_table_card(card_id):
    game_code = st.query_params.game
    table_cards = get_data("table_cards", game_code=game_code)
    if card_id in table_cards:
        table_cards.remove(card_id)
        set_data("table_cards", table_cards, game_code=game_code)
    add_card_to_discard(card_id)
    return


def retain_table_card(card_id):
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


def set_action(card_id):
    card = get_card(card_id)
    action = st.session_state[f"action_{card_id}"]
    st.session_state[f"action_{card_id}"] = None
    if action == "Unselect":
        unselect_card(card_id)
    elif action == "Use to Defend":
        use_card_for_battle(card_id, "defender")
    elif action == "Use to Attack":
        use_card_for_battle(card_id, "attacker")
    elif action == "Discard":
        add_card_to_discard(card_id)
        return
    elif action == "Take for Friendly Exchange":
        card_owner = get_card_owner(card_id)
        transfer_card(card_id)
        add_activity(f"{action} (from {card_owner['character']})")
        return
    elif action == "Place on table":
        place_card_on_table(card_id)
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
        action += f": {roll}"
    add_activity(action)


def show_battle_section():
    game_code = st.query_params.game
    battle = get_data("battle", game_code=game_code)
    battle_roles = ["attacker", "defender"]
    for battle_role in battle_roles:
        if battle[f"{battle_role}_cards"]:
            return True
    return False
