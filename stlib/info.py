import streamlit as st
from sections import navbar


def run():
    st.query_params.page = "info"
    navbar.run()

    about_tab, rules_tab, cards_tab = st.tabs(["About", "Rules", "Cards"])

    with about_tab:
        st.write("About the game")

    with rules_tab:
        st.write("These are the rules")

    with cards_tab:
        st.write("These are the cards")
