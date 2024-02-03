import streamlit as st
from sections import navbar


def run():
    st.query_params.page = "start_new_game"
    navbar.run()
    st.write("Start new game")
    st.write(st.session_state)

    if st.button("Start"):
        st.query_params.page = "play"
        st.query_params.game = "123"
        st.query_params.player = "abc"
        st.rerun()
