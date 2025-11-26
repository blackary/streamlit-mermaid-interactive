export default function(component) {
  const { data, setStateValue, setTriggerValue, parentElement } = component;
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
              const allGs = container.querySelectorAll('g');
              console.log(allGs);
              const entityGroups = [];

              allGs.forEach((g) => {
                  const hasID = g.id != '' || (
                      g.classList.contains('label') && g.classList.contains('name')
                  );
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
                  group.classList.add('mermaid-clickable');

                  group.addEventListener('click', (e) => {
                      e.preventDefault();
                      e.stopPropagation();

                      const originalName = (
                          data.entity_name_mapping ? data.entity_name_mapping[entityName] || entityName : entityName
                      );

                      setStateValue('entity_clicked', originalName);
                      setTriggerValue('clicked', originalName);
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