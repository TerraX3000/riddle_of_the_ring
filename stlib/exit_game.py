import streamlit as st
from sections import navbar
from icecream import ic


def run():
    st.query_params.page = "exit_game"
    navbar.run()
    st.write("Are you sure you want to exit the game?")
    if st.button("Yes - Delete All My Player Info"):
        st.query_params.clear()
        st.session_state.clear()
        st.query_params.page = "index"
        st.rerun()
    if st.button("No - Take Me Back to My Game"):
        st.query_params.page = "play"
        st.rerun()
