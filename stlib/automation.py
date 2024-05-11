import streamlit as st
from streamlit_datatables_net import st_datatable
import os
import json


def add_progam(command, program, schedule, automation_schedule):
    if command and program and schedule:
        automation_program = {}
        automation_program["command"] = command
        automation_program["name"] = program
        automation_program["schedule"] = schedule
        automation_schedule.append(automation_program)
        with open("static/automation_schedule.json", "w") as f:
            json.dump(automation_schedule, f)


def run():
    st.write("Automation Scheduler")
    path = "static/automation_schedule.json"
    if not os.path.exists(path):
        automation_schedule = []
        with open("static/automation_schedule.json", "w") as f:
            json.dump(automation_schedule, f)

    with open("static/automation_schedule.json") as f:
        automation_schedule = json.load(f)
    selected_program = st_datatable(
        automation_schedule, table_id="automation_schedule_table"
    )

    if selected_program:
        st.write(selected_program)

    col_1, col_2, col_3, col_4 = st.columns([1, 1, 1, 1])
    with col_1:
        options = ["automation_script"]
        command = st.selectbox("Type", options=options)
    with col_2:
        options = ["Program A", "Program B", "Program C", "Program D", "Option E"]
        program = st.selectbox("Program Name", options=options)
    with col_3:
        schedule = st.text_input("Schedule", placeholder="* 15 * * *")
    with col_4:
        st.button(
            "Add Program",
            on_click=add_progam,
            args=[command, program, schedule, automation_schedule],
        )
