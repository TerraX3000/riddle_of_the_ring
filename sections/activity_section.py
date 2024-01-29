import streamlit as st
from functions.utility import get_data


def run():
    st.markdown("# Activity Log")
    with st.container(height=1000):
        activities = get_data("activities")
        for activity in reversed(activities):
            activity_markdown = (
                f"""### {activity["player"]["character"]} | {activity["action"]}"""
            )
            st.markdown(activity_markdown)
