import streamlit as st


def run():
    with open("static/documents/RiddleOfTheRing-rules.pdf", "rb") as file:
        btn = st.download_button(
            label="Download Rukes",
            data=file,
            file_name="RiddleOfTheRing.pdf",
            mime="application/pdf",
        )
    # st.download_button("Download Rules", "static/documents/RiddleOfTheRing-rules.pdf")
