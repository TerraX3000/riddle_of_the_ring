import streamlit as st
from functions.utility import get_data, add_activity
import time
from icecream import ic


def stream_data(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.5)


def get_ai_response():
    add_activity(
        "That's an interesting question.  What do you think?", type="assistant"
    )


def get_game_stats():
    game_code = st.query_params.game
    players = get_data("players", game_code=game_code)
    characters = get_data("characters")
    response = """"""
    hobbits = [
        player["character"]
        for player in players.values()
        if characters[player["character"]]["side"] == "good"
    ]
    black_riders = [
        player["character"]
        for player in players.values()
        if characters[player["character"]]["side"] == "evil"
    ]
    if hobbits:
        response += f"""For the Hobbits, we have:\n\n {' '.join(hobbits)}\n\n"""
    else:
        response += f"""There are no Hobbits playing.\n\n"""
    if black_riders:
        response += f"""For the Black Riders, we have:\n\n {' '.join(black_riders)}"""
    else:
        response += f"""There are no Black Riders playing."""
    print(response)

    add_activity(response, type="assistant")


def update_chat_messages(message_container):
    game_code = st.query_params.game
    activities = get_data("activities", game_code=game_code)
    activities = [
        activity for activity in activities if activity.get("type") != "system"
    ]
    for index, activity in enumerate(activities, start=1):
        activity_markdown = (
            f"""{activity["player"]["character"]}: {activity["action"]}"""
        )
        if activity.get("type") == "user":
            message_container.chat_message("user").write(f"{activity_markdown}")
        elif activity.get("type") == "assistant":
            message_container.chat_message("assistant").write(activity["action"])


def run():
    help = "Displays messages from players and game activities.  Type 'm' to check for new messages"
    st.title("Game Chat", help=help)
    messages = st.container(height=300)

    if prompt := st.chat_input("Say something or type 'm' to check for new messages"):
        if prompt.lower() == "stats":
            get_game_stats()
        elif prompt.lower().startswith("ai"):
            cleaned_prompt = prompt.replace("ai", "").strip()
            add_activity(cleaned_prompt, type="assistant")
            get_ai_response()
        elif prompt.lower() != "m":
            add_activity(prompt, type="user")
    update_chat_messages(messages)
