import streamlit as st
from icecream import ic
import json
import os
import datetime

LOG_PATH = "automation_log.json"


def get_automation_log(is_reset_log=False):
    if not os.path.exists(LOG_PATH) or is_reset_log:
        automation_log = []
        with open(LOG_PATH, "w") as f:
            json.dump(automation_log, f)

    with open(LOG_PATH, "r") as f:
        automation_log = json.load(f)
    return automation_log


def add_log_entry(log_entry):
    timestamp = datetime.datetime.now()
    log_entry = {"automation_log": log_entry, "timestamp": str(timestamp)}
    automation_log = get_automation_log()
    automation_log.append(log_entry)
    with open(LOG_PATH, "w") as f:
        json.dump(automation_log, f)
    return True


def run():
    query_params = st.query_params.to_dict()
    log_entry = query_params.get("log")
    if log_entry:
        add_log_entry(log_entry)
    else:
        reset_log = st.button("Reset log")
        if reset_log:
            get_automation_log(is_reset_log=True)
        automation_log = get_automation_log()
        st.write(automation_log)
