# Streamlit Mermaid Interactive

A Streamlit component for rendering interactive Mermaid diagrams with click event handling.

## Installation

with uv:
```bash
uv add streamlit-mermaid-interactive
```
with pip:
```bash
pip install streamlit-mermaid-interactive
```

## Demo

https://mermaid-component.streamlit.app/

## Supported Diagram Types

This component currently supports **5 diagram types** with full interactivity:

### ✅ Fully Working

1. **Flowchart** - Click on nodes
2. **Sequence Diagram** - Click on actors/participants
3. **Entity Relationship Diagram (ERD)** - Click on entity boxes
4. **State Diagram** - Click on state boxes
5. **Class Diagram** - Click on class boxes

### ⚠️ Rendered but Not Interactive

The following diagram types are **rendered correctly** but **clicks do not yet work**:

1. **Pie Chart** - Legend items not yet clickable
2. **Gantt Chart** - No identifiable parent containers for tasks
3. **Git Graph** - Commits without IDs have no clickable targets
4. **User Journey** - Task text elements lack identifiable parents
5. **Timeline** - Text elements have no IDs or clickable parents

## Usage

```python
import streamlit as st
from streamlit_mermaid_interactive import mermaid

# Example: Flowchart
flowchart_code = """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[OK]
    B -->|No| D[End]
"""

result = mermaid(flowchart_code, theme="neutral", key="flowchart")

if result.get("entity_clicked"):
    st.info(f"Clicked: {result['entity_clicked']}")
```

## Supported Themes

- `"neutral"` (default)
- `"dark"`
- `"forest"`
- `"base"`

## Known Limitations

### Technical Challenges

The unsupported diagram types have specific issues with Mermaid 11's SVG rendering:

- **Pie Charts**: Legend items not structured for easy click detection
- **Gantt Charts**: Task rectangles exist but have no parent containers with IDs
- **Git Graphs**: Commits created with bare `commit` command have no commit IDs to extract
- **User Journey/Timeline**: Text elements for tasks/events have no identifiable parent elements with IDs

### Why Not More Diagrams?

Mermaid uses different SVG structures for different diagram types. Some structures make it straightforward to identify clickable elements (like ERD entity boxes or State diagram states), while others require complex DOM traversal or text-based parsing that is error-prone.

## Development

### Building the Frontend

The component uses Vite to bundle the frontend JavaScript with Mermaid 11:

```bash
# Install dependencies (first time only)
npm install

# Build the frontend
npm run build
```

After editing `src/streamlit_mermaid_interactive/frontend/component.js`, run `npm run build` to rebuild `main.js`.

### Running Tests

```bash
# Run tests
uv run pytest
```

### Manual Testing

Run the demo app:
```bash
streamlit run streamlit_app.py
```

To add support for more diagram types, you would need to:

1. Inspect the SVG structure for that diagram type
2. Find a reliable selector or ID pattern for clickable elements
3. Update the click detection logic in `src/streamlit_mermaid_interactive/frontend/component.js`
4. Rebuild the frontend with `npm run build`
5. Test thoroughly with various diagram configurations

## Example App

See `streamlit_app.py` for examples of all diagram types (both working and non-working).

## License

MIT
