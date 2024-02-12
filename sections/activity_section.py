import streamlit as st
from functions.utility import get_data, add_activity


def update_chat_messages(message_container):
    game_code = st.query_params.game
    activities = get_data("activities", game_code=game_code)

    for index, activity in enumerate(activities):
        activity_markdown = (
            f"""{activity["player"]["character"]}: {activity["action"]}"""
        )
        if activity.get("type") == "user":
            message_container.chat_message("user").write(f"{activity_markdown}")
        else:
            message_container.chat_message("assistant").write(f"{activity_markdown}")


def run():
    help = "Displays messages from players and game activities.  Type 'm' to check for new messages"
    st.title("Messages", help=help)
    messages = st.container(height=300)
    update_chat_messages(messages)

    if prompt := st.chat_input("Say something or type 'm' to check for new messages"):
        if prompt.lower() != "m":
            add_activity(prompt, type="user")
        update_chat_messages(messages)
