# progress.py — progress tracking via localStorage using Streamlit custom component

import streamlit as st
import streamlit.components.v1 as components
import json

STORAGE_KEY = "math_tutor_v1"

def _sync_component(visited_list, key_suffix=""):
    """Render a hidden component that syncs with localStorage."""
    visited_json = json.dumps(visited_list)
    result = components.html(f"""
<!DOCTYPE html>
<html>
<head><style>body{{margin:0;padding:0;}}</style></head>
<body>
<script>
(function() {{
    const STORAGE_KEY = "{STORAGE_KEY}";

    // Read current from localStorage
    let stored = [];
    try {{
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) stored = JSON.parse(raw);
    }} catch(e) {{}}

    // Merge with what Streamlit sent
    const fromPython = {visited_json};
    const merged = Array.from(new Set([...stored, ...fromPython]));

    // Save merged back
    localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));

    // Send merged list back to Streamlit
    window.parent.postMessage({{
        type: "streamlit:setComponentValue",
        value: JSON.stringify(merged)
    }}, "*");
}})();
</script>
</body>
</html>
""", height=0, key=f"progress_sync_{key_suffix}")
    return result


def load_and_sync():
    """
    On first load: read localStorage and merge into session_state.
    Call this once at the top of app.py.
    """
    if "visited" not in st.session_state:
        st.session_state["visited"] = set()

    # Only sync on first render per session
    if st.session_state.get("_progress_synced"):
        return

    visited_list = sorted(list(st.session_state["visited"]))
    result = _sync_component(visited_list, key_suffix="init")

    if result:
        try:
            merged = json.loads(result)
            st.session_state["visited"] = set(merged)
        except Exception:
            pass

    st.session_state["_progress_synced"] = True


def mark_visited(n: int):
    """Mark module n as visited and persist to localStorage."""
    if "visited" not in st.session_state:
        st.session_state["visited"] = set()
    st.session_state["visited"].add(n)

    visited_list = sorted(list(st.session_state["visited"]))
    _sync_component(visited_list, key_suffix=str(n))


def is_visited(n: int) -> bool:
    return n in st.session_state.get("visited", set())


def get_visited() -> set:
    return st.session_state.get("visited", set())


def reset_progress():
    """Clear all progress from session and localStorage."""
    st.session_state["visited"] = set()
    st.session_state["_progress_synced"] = False
    components.html(f"""
<!DOCTYPE html>
<html><body>
<script>localStorage.removeItem("{STORAGE_KEY}");</script>
</body></html>
""", height=0, key="progress_reset")