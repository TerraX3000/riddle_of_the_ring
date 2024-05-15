import streamlit as st
import os
import json
import uuid

schedule_path = "static/automation_schedule.json"


def clear_schedule():
    with open(schedule_path, "w") as f:
        json.dump([], f)


def add_progam(command, program, schedule, automation_schedule):
    if command and program and schedule:
        automation_program = {}
        automation_program["uid"] = str(uuid.uuid4())
        automation_program["command"] = command
        automation_program["name"] = program
        automation_program["schedule"] = schedule
        automation_schedule.append(automation_program)
        with open(schedule_path, "w") as f:
            json.dump(automation_schedule, f)


def run():
    st.write("Automation Scheduler")
    if not os.path.exists(schedule_path):
        automation_schedule = []
        with open(schedule_path, "w") as f:
            json.dump(automation_schedule, f)

    with open(schedule_path) as f:
        automation_schedule = json.load(f)

    st.button("Clear Schedule", on_click=clear_schedule)

    st.data_editor(automation_schedule, use_container_width=True)

    col_1, col_2, col_3, col_4 = st.columns([1, 1, 1, 1])
    with col_1:
        options = ["automation_script"]
        command = st.selectbox("Type", options=options)
    with col_2:
        options = ["Program 1", "Program 2", "Program 3", "Program 4", "Program 5"]
        program = st.selectbox("Program Name", options=options)
    with col_3:
        schedule = st.text_input("Schedule", placeholder="* 15 * * *")

    st.button(
        "Add Program",
        on_click=add_progam,
        args=[command, program, schedule, automation_schedule],
    )
