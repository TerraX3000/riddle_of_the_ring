import streamlit as st


def show_section(filename, container):
    with container:
        col_1, col_2, col_3 = st.columns([2, 8, 2])
        with col_2:
            with open(f"data/rules/{filename}") as f:
                for line in f.readlines():
                    st.markdown(line)


def run(area):
    sections = {
        "INTRODUCTION": {"INTRODUCTION": "introduction.txt"},
        "THE BASIC GAME": {
            "THE BASIC GAME": "basic game/b0.txt",
            "B-1 THE GAME COMPONENTS": "basic game/b1.txt",
            "B-2 Starting The Game": "basic game/b2.txt",
            "B-3 How To Win The Game": "basic game/b3.txt",
            "B-4 What To Do During A Turn": "basic game/b4.txt",
            "B-5 Moving A Marker": "basic game/b5.txt",
            "B-6 The Spaces On The Board": "basic game/b6.txt",
            "B-7 Using The Cards": "basic game/b7.txt",
            "B-8 How To Use The Cards": "basic game/b8.txt",
            "B-9 Friendly Exchanges": "basic game/b9.txt",
            "B-10 Power Plays": "basic game/b10.txt",
            "B-11 Battles": "basic game/b11.txt",
            "B-12 The Halls Of Mandos (The Other World)": "basic game/b12.txt",
        },
    }
    columns_row_1 = st.columns([1, 1, 1, 1, 1, 1, 1])
    columns_row_2 = st.columns([1, 1, 1, 1, 1, 1, 1])
    text_container = st.empty()
    if len(sections[area].keys()) > 1:
        for (section_name, filename), column in zip(
            sections[area].items(), columns_row_1 + columns_row_2
        ):
            with column:
                if st.button(
                    section_name,
                    use_container_width=True,
                ):
                    show_section(filename, text_container)
    elif len(sections[area].keys()) == 1:
        for filename in sections[area].values():
            show_section(filename, text_container)
