import streamlit as st

from streamlit_mermaid_interactive import mermaid

st.title("Interactive Mermaid Diagrams")

# Segmented control for diagram type selection
diagram_type = st.segmented_control(
    "Select diagram type",
    options=["Flowchart", "State Diagram", "ERD", "Sequence", "Class Diagram"],
    default="Flowchart",
)

if diagram_type == "Flowchart":
    st.header("Flowchart (Neutral Theme)")
    selected_item = st.session_state.get("flowchart", {}).get("entity_clicked", None)
    mapping = {
        "A": "Start",
        "B": "Is it?",
        "C": "OK",
        "D": "Rethink",
        "E": "End",
    }
    reversed_mapping = {v: k for k, v in mapping.items()}

    with st.echo(code_location="below"):
        flowchart_code = """
graph TD
    A[Start] --> B{Is it?}
    B -->|Yes| C[OK]
    C --> D[Rethink]
    D --> B
    B ---->|No| E[End]
"""
        # Add style to the selected item, if any
        if selected_item:
            flowchart_code += f"\nstyle {reversed_mapping[selected_item]} fill:#f9f,stroke:#333,stroke-width:4px"

        def on_click():
            item_clicked = st.session_state["flowchart"]["clicked"]
            st.toast(f"Clicked: {item_clicked}")

        entities = mermaid(
            flowchart_code,
            theme="neutral",
            key="flowchart",
            on_click=on_click,
        )
        if clicked := entities.get("entity_clicked"):
            st.info(f"Flowchart - Clicked: {clicked}")
        else:
            st.info(":material/touch_app: Click on any node in the diagram")

elif diagram_type == "State Diagram":
    st.header("State Diagram (Dark Theme)")
    with st.echo(code_location="below"):
        state_code = """
stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
"""
        entities = mermaid(state_code, theme="dark", key="state")
        if clicked := entities.get("entity_clicked"):
            st.info(f"State Diagram - Clicked: {clicked}")
        else:
            st.info(":material/touch_app: Click on any node in the diagram")

elif diagram_type == "ERD":
    st.header("Entity Relationship Diagram (Default Theme)")
    with st.echo(code_location="below"):
        erd_code = """
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
    CUSTOMER {
        string name
        string custNumber
        string sector
    }
    ORDER {
        int orderNumber
        string deliveryAddress
    }
    LINE-ITEM {
        string productCode
        int quantity
        float pricePerUnit
    }
"""
        entities = mermaid(erd_code, key="erd")
        if clicked := entities.get("entity_clicked"):
            st.info(f"ERD - Clicked: {clicked}")
        else:
            st.info(":material/touch_app: Click on any entity in the diagram")

elif diagram_type == "Sequence":
    st.header("Sequence Diagram (Forest Theme)")
    with st.echo(code_location="below"):
        sequence_code = """
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Hello John, how are you?
    loop Healthcheck
        John->>John: Fight against hypochondria
    end
    Note right of John: Rational thoughts!
    John-->>Alice: Great!
    John->>Bob: How about you?
    Bob-->>John: Jolly good!
"""
        entities = mermaid(sequence_code, theme="forest", key="sequence")
        if clicked := entities.get("entity_clicked"):
            st.info(f"Sequence - Clicked: {clicked}")
        else:
            st.info(":material/touch_app: Click on any element in the diagram")

elif diagram_type == "Class Diagram":
    st.header("Class Diagram (Base Theme)")
    with st.echo(code_location="below"):
        class_code = """
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal <|-- Zebra
    Animal : +int age
    Animal : +String gender
    Animal: +isMammal()
    Animal: +mate()
    class Duck{
        +String beakColor
        +swim()
        +quack()
    }
    class Fish{
        -int sizeInFeet
        -canEat()
    }
    class Zebra{
        +bool is_wild
        +run()
    }
"""
        entities = mermaid(class_code, theme="base", key="class")
        if clicked := entities.get("entity_clicked"):
            st.info(f"Class Diagram - Clicked: {clicked}")
        else:
            st.info(":material/touch_app: Click on any class in the diagram")
