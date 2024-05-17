import streamlit as st
import os
import json
import uuid

schedule_path = "static/automation_schedule.json"


def clear_schedule():
    with open(schedule_path, "w") as f:
        json.dump({}, f)


def add_progam():
    if not st.session_state.program:
        st.error("Program is required")
    else:
        automation_schedule = st.session_state.automation_schedule
        schedule = f"{st.session_state.minute} {st.session_state.hour} {st.session_state.day_of_month} {st.session_state.month} {st.session_state.day_of_week}"
        print(schedule)
        uid = str(uuid.uuid4())
        automation_program = {}
        automation_program["uid"] = uid
        automation_program["command"] = st.session_state.command
        automation_program["name"] = st.session_state.program
        automation_program["schedule"] = schedule
        automation_schedule[uid] = automation_program
        with open(schedule_path, "w") as f:
            json.dump(automation_schedule, f)


def run():
    st.write("Automation Scheduler")
    if not os.path.exists(schedule_path):
        automation_schedule = {}
        with open(schedule_path, "w") as f:
            json.dump(automation_schedule, f)

    with open(schedule_path) as f:
        automation_schedule = json.load(f)

    st.button("Clear Schedule", on_click=clear_schedule)
    st.session_state.automation_schedule = automation_schedule
    st.data_editor(list(automation_schedule.values()), use_container_width=True)
    with st.form(key="add_program_form", clear_on_submit=True):
        col_1, col_2 = st.columns(
            [
                1,
                1,
            ]
        )
        col_3, col_4, col_5, col_6, col_7 = st.columns([1, 1, 1, 1, 1])
        with col_1:
            options = ["automation_script"]
            st.selectbox("Type", options=options, disabled=True, key="command")
        with col_2:
            options = [
                "Program 1",
                "Program 2",
                "Program 3",
                "Program 4",
                "Program 5",
                "Power Off",
            ]
            st.selectbox("Program Name", options=options, index=None, key="program")
        with col_3:
            st.text_input("Minute (0-59)", value="*", key="minute")
        with col_4:
            st.text_input("Hour (0-23)", value="*", key="hour")
        with col_5:
            st.text_input("Day of Month (1-31)", value="*", key="day_of_month")
        with col_6:
            st.text_input("Month (1-12)", value="*", key="month")
        with col_7:
            st.text_input("Day of Week (0-6)", value="*", key="day_of_week")

        st.form_submit_button("Add Program", on_click=add_progam)
