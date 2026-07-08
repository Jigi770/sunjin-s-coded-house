from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FOR HIM - Men's Beauty AI Demo", layout="wide")

html_path = Path(__file__).parent / "demo.html"
html_content = html_path.read_text(encoding="utf-8")

components.html(html_content, height=900, scrolling=False)
