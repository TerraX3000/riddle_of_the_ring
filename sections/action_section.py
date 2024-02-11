import streamlit as st
from sections import action_general_subsection, action_card_subsection


def run():
    with st.container(border=True):
        action_general_subsection.run()

    with st.container(border=True):
        action_card_subsection.run()
