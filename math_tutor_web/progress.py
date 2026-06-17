# progress.py — session-based progress tracking (no localStorage)

import streamlit as st

def load_and_sync():
    """Initialize visited set in session state."""
    if "visited" not in st.session_state:
        st.session_state["visited"] = set()

def mark_visited(n: int):
    if "visited" not in st.session_state:
        st.session_state["visited"] = set()
    st.session_state["visited"].add(n)

def is_visited(n: int) -> bool:
    return n in st.session_state.get("visited", set())

def get_visited() -> set:
    return st.session_state.get("visited", set())

def reset_progress():
    st.session_state["visited"] = set()