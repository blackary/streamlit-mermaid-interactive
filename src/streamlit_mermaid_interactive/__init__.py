import hashlib
from typing import Callable

import streamlit as st


def get_mermaid_component(opacity: float = 0.5):
    return st.components.v2.component(
        "streamlit_mermaid_interactive.mermaid",
        html="""
        <div id="mermaid-container"></div>
        """,
        css=f"""
        #mermaid-container {{width: 100%;height: 100%;}}
        .mermaid-clickable {{transition: opacity 0.2s ease;}}
        .mermaid-clickable:hover {{opacity: {opacity} !important;}}
        """,
        js="main.js",
    )


def mermaid(
    mermaid_code: str,
    entity_name_mapping: dict | None = None,
    theme: str = "neutral",
    selected_entity: str | None = None,
    key: str | None = None,
    on_click: Callable[..., None] | None = None,
    hover_opacity: float = 0.5,
):
    """
    Render a Mermaid ERD diagram.
    """
    data = {
        "mermaid_code": mermaid_code,
        "selected_entity": selected_entity,
        "entity_name_mapping": entity_name_mapping,
        "theme": theme,
        "hover_opacity": hover_opacity,
    }
    if not key:
        # Hash the mermaid code
        key = "mermaid-" + hashlib.sha256(mermaid_code.encode()).hexdigest()
    return get_mermaid_component(opacity=hover_opacity)(
        data=data,
        key=key,
        on_clicked_change=on_click,
    )
