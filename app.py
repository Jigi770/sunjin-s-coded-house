from pathlib import Path

import streamlit as st

st.set_page_config(page_title="FOR HIM - Men's Beauty AI Demo", layout="wide")

html_path = Path(__file__).parent / "demo.html"

st.iframe(html_path, height="content", width="stretch")
