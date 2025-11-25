def test_import():
    from streamlit_mermaid_interactive import mermaid

    assert mermaid is not None


def test_mermaid_component():
    from streamlit_mermaid_interactive import mermaid

    mermaid_code = """
    graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
    """
    mermaid(mermaid_code, theme="neutral", key="flowchart")
