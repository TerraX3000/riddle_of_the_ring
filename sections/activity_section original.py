import streamlit as st
from functions.utility import get_data


def run():
    st.markdown("# Activity Log")
    game_code = st.query_params.game
    with st.container(height=1000):
        activities = get_data("activities", game_code=game_code)
        num_activities = len(activities)
        for index, activity in enumerate(reversed(activities)):
            activity_markdown = f"""#### {num_activities - index} | {activity["player"]["character"]} | {activity["action"]}"""
            st.markdown(activity_markdown)
