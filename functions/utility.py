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


def initialize_game_data(data=None, *, category: str):
    if data is None:
        with open(f"data/{category}.yaml") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
    redis_functions.set_data(category, json.dumps(data))


def get_data(category: str):
    data = redis_functions.get_data(category)
    # print("get_data", category, data)
    if data is not None:
        return json.loads(data)
    return data
    # with open(f"data/{category}.yaml") as f:
    #     data = yaml.load(f, Loader=yaml.SafeLoader)
    # return data


def set_data(category: str, data):
    redis_functions.set_data(category, json.dumps(data))


def get_item(category: str, id: int):
    items = get_data(category)
    for item in items:
        if item["id"] == id:
            return item
    return None


def add_activity(player, action):
    activities = get_data("activities")
    activity = {"player": player, "action": action}
    activities.append(activity)
    set_data("activities", activities)


@st.cache_data
def get_cards():
    print("cached cards")
    with open(f"data/cards.yaml") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data
    # return get_data("cards")


def get_card_owner(card_id):
    players = get_data("players")
    for player in players:
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


def get_player_cards(player_id: str = None, character: str = None):
    if player_id:
        player = get_item("players", player_id)
        if player:
            return player["cards"]
        return None
    elif character:
        players = get_data("players")
        for player in players:
            if player["character"] == character:
                return player["cards"]
        return None


def add_selected_card(card_id):
    st.session_state["selected_cards"].append(card_id)


def unselect_card(card_id):
    if card_id in st.session_state["selected_cards"]:
        st.session_state["selected_cards"].remove(card_id)


def unselect_all_cards():
    selected_cards = st.session_state["selected_cards"].copy()
    for card_id in selected_cards:
        unselect_card(card_id)


# def add_in_use_card(card_id):
#     unselect_card(card_id=card_id)
#     st.session_state["in_use_cards"].append(card_id)


def is_card_selected(card_id):
    if card_id in st.session_state["selected_cards"]:
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
    draw_pile = get_data("draw_pile")
    draw_cards = []
    for x in range(number):
        draw_cards.append(draw_pile.pop())
    set_data("draw_pile", draw_pile)
    this_player = st.session_state["player"]
    players = get_data("players")
    for player in players:
        if player["id"] == this_player["id"]:
            player["cards"].extend(draw_cards)
    set_data("players", players)
    return draw_cards


def update_players(players):
    set_data("players", players)


def remove_card_from_hand(card_id):
    this_player = st.session_state["player"]
    players = get_data("players")
    for player in players:
        if player["id"] == this_player["id"]:
            if card_id in player["cards"]:
                player["cards"].remove(card_id)
                set_data("players", players)


def add_card_to_discard(card_id):
    unselect_card(card_id)
    discards = get_data("discards")
    discards.append(card_id)
    set_data("discards", discards)
    remove_card_from_hand(card_id)


def keep_card(card_id):
    if card_id in st.session_state["in_use_cards"]:
        st.session_state["in_use_cards"].remove(card_id)
    print(f"keeping card {card_id}")


def use_card_for_battle(card_id, battle_role):
    st.session_state[f"{battle_role}_cards"].append(card_id)


def remove_battle_card(card_id, battle_role):
    if card_id in st.session_state[f"{battle_role}_cards"]:
        st.session_state[f"{battle_role}_cards"].remove(card_id)


def discard_battle_card(card_id, battle_role):
    add_card_to_discard(card_id)
    if card_id in st.session_state[f"{battle_role}_cards"]:
        st.session_state[f"{battle_role}_cards"].remove(card_id)


def retain_battle_card(card_id, battle_role):
    if card_id in st.session_state[f"{battle_role}_cards"]:
        st.session_state[f"{battle_role}_cards"].remove(card_id)


def add_city_battle_card(battle_role, side):
    if side == "good":
        card_id = 24
    if side == "evil":
        card_id = 25
    use_card_for_battle(card_id, battle_role)


def set_action(card_id):
    card = get_card(card_id)
    action = st.session_state[f"action_{card_id}"]
    if action == "Unselect":
        unselect_card(card_id)
    elif action == "Use to Defend":
        use_card_for_battle(card_id, "defender")
    elif action == "Use to Attack":
        use_card_for_battle(card_id, "attacker")
    elif action == "Discard":
        add_card_to_discard(card_id)
    st.session_state[f"action_{card_id}"] = None
    player = st.session_state["player"]
    add_activity(player, f"{action} ({card['name']})")


def set_general_action():
    action = st.session_state[f"general_action"]
    print(action)
    if action == "Attack from Good City":
        add_city_battle_card("attacker", "good")
    elif action == "Attack from Evil City":
        add_city_battle_card("attacker", "evil")
    elif action == "Defend from Good City":
        add_city_battle_card("defender", "good")
    elif action == "Defend from Evil City":
        add_city_battle_card("defender", "evil")
    elif action == "Show Hand to Player":
        st.info("Show Hand to Player", icon="ℹ️")
    elif action == "Draw Card":
        draw_cards(1)
    st.session_state[f"general_action"] = None
    player = st.session_state["player"]
    add_activity(player, action)


def show_battle_section():
    battle_roles = ["attacker", "defender"]
    for battle_role in battle_roles:
        if st.session_state[f"{battle_role}_cards"]:
            return True
    return False
