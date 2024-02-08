import streamlit as st
from sections import navbar
from functions.utility import (
    get_data,
    set_data,
    initialize_game_data,
    get_shuffled_deck,
)
from icecream import ic
import coolname


@st.cache_data(ttl=600)
def get_code_options(id: str = None):
    codes = coolname.generate()
    codes = [code for code in codes if len(code) > 2]
    return codes


def initialize_game(game_code, player_code, character):
    if "is_initialized" not in st.session_state:
        print("+++++ Initializing session +++++++")
        st.session_state["is_initialized"] = True
        st.session_state["points"] = []

        players = {}
        player = {
            "id": 0,
            "name": "P1",
            "character": character,
            "current_turn": False,
            "cards": [],
            "selected_cards": [],
            "player_code": player_code,
            "positions": [],
            "special_actions": {"show_hand_to_character": None},
        }
        players[player_code] = player
        initialize_game_data(category="players", game_code=game_code, data=players)
        initialize_game_data(category="activities", game_code=game_code, data=[])
        initialize_game_data(
            category="draw_pile", game_code=game_code, data=get_shuffled_deck()
        )
        initialize_game_data(category="discards", game_code=game_code, data=[])
        battle = {"attacker_cards": [], "defender_cards": []}
        initialize_game_data(category="battle", data=battle, game_code=game_code)
        initialize_game_data(category="table_cards", data=[], game_code=game_code)
        game = {"is_started": False}
        initialize_game_data(category="game", data=game, game_code=game_code)

        print("+++++ Session initialization complete +++++++")

        games = get_data("games")
        game = {"game_code": game_code}
        games.append(game)
        set_data("games", games)
        return


def initialize_player(game_code, player_code, character):
    st.session_state["is_initialized"] = True
    st.session_state["points"] = []
    players = get_data("players", game_code=game_code)

    player = {
        "id": len(players),
        "name": "P1",
        "character": character,
        "current_turn": False,
        "cards": [],
        "selected_cards": [],
        "player_code": player_code,
        "positions": [],
        "special_actions": {"show_hand_to_character": None},
    }
    players[player_code] = player
    set_data(category="players", data=players, game_code=game_code)


def run():
    st.query_params.page = "start_or_join_game"
    sid = st.session_state.sid
    navbar.run()

    start_new_game, join_game = st.tabs(["Start New Game", "Join with Game Code"])

    with start_new_game:
        st.header("Start New Game")
        characters = get_data("characters").keys()
        selected_character = st.radio(
            "Choose Your Character", options=characters, key="start_as_character"
        )
        st.write("Share the Game Code with your fellow players so they can join")
        game_code = st.radio(
            "Choose Game Code", options=get_code_options(f"{sid}-game")
        )
        st.write(
            "Use the Player Code to resume the game as your character if you reload the site"
        )
        player_code = st.radio(
            "Choose Player Code",
            options=get_code_options(f"{sid}-start_player"),
            key="start_player_code",
        )

        if st.button("Begin the Quest"):
            st.query_params.page = "play"
            st.query_params.game = game_code
            st.query_params.player = player_code
            initialize_game(game_code, player_code, selected_character)
            st.rerun()

    with join_game:
        st.header("Join with Game Code")
        code_column, unused = st.columns([2, 10])
        with code_column:
            game_code = st.text_input("Enter Game Code").lower()

            if game_code:
                games = get_data("games")
                valid_game_codes = [game["game_code"] for game in games]
                if game_code in valid_game_codes:
                    characters = get_data("characters").keys()
                    selected_character = st.radio(
                        "Choose Your Character",
                        options=characters,
                        key="join_as_character",
                    )
                    st.write(
                        "Use the Player Code to resume the game as your character if you reload the site"
                    )
                    player_code = st.radio(
                        "Choose Player Code",
                        options=get_code_options(f"{sid}-join_player"),
                        key="join_player_code",
                    )
                    if st.button("Join the Quest"):

                        st.query_params.page = "play"
                        st.query_params.game = game_code
                        st.query_params.player = player_code
                        initialize_player(game_code, player_code, selected_character)
                        st.rerun()
                else:
                    st.error("That's not a valid game code")
