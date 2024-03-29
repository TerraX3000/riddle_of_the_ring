import importlib
from functions.utility import get_app_config, validate_game_data
import streamlit as st
import uuid

st.set_page_config(
    page_title="Riddle of the Ring",
    layout="wide",
)

if "sid" not in st.session_state:
    st.session_state.sid = str(uuid.uuid4())

validate_game_data()

module_names = get_app_config(config_name="modules")
try:
    module_name = st.query_params["page"]
except:
    module_name = "index"

if module_name:
    if module_name in module_names:
        module = importlib.import_module(f"stlib.{module_name}")
        module.run()
    else:
        st.error(
            f'Module named "{module_name}" not found.  Did you forget to add it to the config file?'
        )

if module_name is None:
    st.error("Did you forget to set the page?")
