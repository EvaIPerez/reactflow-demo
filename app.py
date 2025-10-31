import streamlit as st

st.set_page_config(page_title="React Flow Demo", layout="wide")
st.markdown("### 🧠 React Flow Diagram Example")

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>React Flow Minimal Example</title>
    <link
      rel="stylesheet"
      href="https://unpkg.com/reactflow@11.10.2/dist/style.css"
    />
    <style>
      html, body, #root {
        height: 100%;
        margin: 0;
        background-color: #f5f5f5;
        font-family: sans-serif;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>

    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/reactflow@11.10.2/dist/reactflow.min.js"></script>

    <script type="text/javascript">
      const { ReactFlow, Background, Controls } = window.ReactFlow;

      const nodes = [
        { id: '1', position: { x: 50, y: 100 }, data: { label: 'Start' } },
        { id: '2', position: { x: 250, y: 100 }, data: { label: 'Process' } },
        { id: '3', position: { x: 450, y: 100 }, data: { label: 'End' } }
      ];

      const edges = [
        { id: 'e1-2', source: '1', target: '2' },
        { id: 'e2-3', source: '2', target: '3' }
      ];

      function App() {
        return React.createElement(
          'div',
          { style: { width: '100%', height: '100%' } },
          React.createElement(
            ReactFlow,
            { nodes, edges, fitView: true },
            React.createElement(Background, null),
            React.createElement(Controls, null)
          )
        );
      }

      const root = ReactDOM.createRoot(document.getElementById('root'));
      root.render(React.createElement(App));
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=600, scrolling=False)

 
