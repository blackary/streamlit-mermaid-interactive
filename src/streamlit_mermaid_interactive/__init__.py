import hashlib

import streamlit as st


def _mermaid_component():
    """
    Create a Streamlit v2 component for rendering interactive Mermaid diagram.
    Returns:
        A Streamlit component function that can be called with:
        - data: dict containing 'mermaid_code', 'selected_entity', 'name_mapping'
        - theme: str for the theme of the diagram
        - key: str for the key of the component
    """
    return st.components.v2.component(
        "mermaid",
        html="""
        <div id="mermaid-container"></div>
        """,
        css="""
        #mermaid-container {
            width: 100%;
            height: 100%;
        }
        """,
        js="""
        export default function(component) {
            const { data, setStateValue, parentElement } = component;
            const container = parentElement.querySelector('#mermaid-container');

            // Check if Mermaid is already loaded
            if (typeof window.mermaid === 'undefined') {
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
                script.onload = () => initializeDiagram();
                document.head.appendChild(script);
            } else {
                initializeDiagram();
            }

            function initializeDiagram() {
                mermaid.initialize({ startOnLoad: false, theme: data.theme || 'neutral' });

                const diagramId = 'mermaid-' + Math.random().toString(36).substr(2, 9);

                mermaid.render(diagramId, data.mermaid_code).then(({svg}) => {
                    container.innerHTML = svg;

                    setTimeout(() => {
                        setStateValue('entity_clicked', null);
                        const allGs = container.querySelectorAll('g');
                        console.log(allGs);
                        const entityGroups = [];

                        allGs.forEach((g) => {
                            // const hasEntityBox = g.querySelector('rect.er.entityBox');
                            const hasID = g.id != '' || g.classList.contains('label');
                            console.log(hasID);
                            if (hasID) {
                                entityGroups.push(g);
                            }
                        });

                        entityGroups.forEach((group) => {
                            let entityName = '';
                            const textElements = group.querySelectorAll('text');
                            const nodeLabels = group.querySelectorAll('.nodeLabel');
                            const labels = group.querySelectorAll('.label');

                            if (textElements.length > 0) {
                                entityName = textElements[0].textContent.trim();
                            }
                            else if (nodeLabels.length > 0) {
                                entityName = nodeLabels[0].textContent.trim();
                            }
                            else if (labels.length > 0) {
                                entityName = labels[0].textContent.trim();
                            }

                            if (!entityName && group.hasAttribute('data-id')) {
                                entityName = group.getAttribute('data-id');
                            }

                            if (!entityName) return;

                            group.style.cursor = 'pointer';
                            group.addEventListener('click', (e) => {
                                e.preventDefault();
                                e.stopPropagation();

                                const originalName = (
                                    data.entity_name_mapping ? data.entity_name_mapping[entityName] || entityName : entityName
                                );

                                setStateValue('entity_clicked', originalName);
                            });
                        });
                    }, 500);
                }).catch(err => {
                    container.innerHTML = (
                        '<p style="color: red;">Error rendering diagram: ' +
                        err.message +
                        '</p>'
                    );
                    console.error('Mermaid error:', err);
                });
            }
        }
        """,
    )


def mermaid(
    mermaid_code: str,
    entity_name_mapping: dict | None = None,
    theme: str = "neutral",
    selected_entity: str | None = None,
    key: str | None = None,
):
    """
    Render a Mermaid ERD diagram.
    """
    data = {
        "mermaid_code": mermaid_code,
        "selected_entity": selected_entity,
        "entity_name_mapping": entity_name_mapping,
        "theme": theme,
    }
    if not key:
        # Hash the mermaid code
        key = "mermaid-" + hashlib.sha256(mermaid_code.encode()).hexdigest()
    return _mermaid_component()(
        data=data,
        key=key,
    )
