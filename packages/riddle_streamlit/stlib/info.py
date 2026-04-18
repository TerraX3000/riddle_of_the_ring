import streamlit as st
from sections import navbar
from sections import info_card_library, info_rules, info_rules_download


def run():
    st.query_params.page = "info"
    navbar.run()

    intro_tab, download_tab, basic_tab, advanced_tab, optional_tab, cards_tab = st.tabs(
        [
            "Introduction",
            "Download Rules",
            "Basic Game",
            "Advanced Game",
            "Optional Rules",
            "Cards",
        ]
    )

    with intro_tab:
        info_rules.run("INTRODUCTION")

    with download_tab:
        info_rules_download.run()

    with basic_tab:
        info_rules.run("THE BASIC GAME")

    with cards_tab:
        info_card_library.run()
