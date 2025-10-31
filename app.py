import streamlit as st

st.set_page_config(page_title="React Flow Demo", layout="wide")

st.markdown("### 🧠 React Flow Diagram Example")

# --- Updated embedded HTML for Streamlit Cloud ---
reactflow_html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>React Flow Diagram</title>
    <style>
      html, body, #root {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
      }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/reactflow/dist/style.css" />
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/reactflow/dist/reactflow.min.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script>
      const { ReactFlow, Background, Controls } = window.ReactFlow;
      const nodes = [
        { id: '1', position: { x: 50, y: 100 }, data: { label: 'Start' } },
        { id: '2', position: { x: 300, y: 100 }, data: { label: 'Process' } },
        { id: '3', position: { x: 550, y: 100 }, data: { label: 'End' } },
      ];
      const edges = [
        { id: 'e1-2', source: '1', target: '2' },
        { id: 'e2-3', source: '2', target: '3' },
      ];

      const App = () => {
        return React.createElement(
          ReactFlow,
          { nodes, edges, fitView: true },
          React.createElement(Background, null),
          React.createElement(Controls, null)
        );
      };

      const root = ReactDOM.createRoot(document.getElementById('root'));
      root.render(React.createElement(App));
    </script>
  </body>
</html>
"""

st.components.v1.html(reactflow_html, height=600, scrolling=False)
