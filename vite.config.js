import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: 'src/streamlit_mermaid_interactive/frontend/component.js',
      name: 'StreamlitMermaidComponent',
      fileName: () => 'main.js',
      formats: ['es']
    },
    outDir: 'src/streamlit_mermaid_interactive/frontend',
    emptyOutDir: false,
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    }
  }
})
