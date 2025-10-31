import streamlit as st

st.set_page_config(page_title="Interactive React Flow", layout="wide")
st.markdown("### 🧠 Interactive React Flow Diagram")

html_code = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>React Flow Demo</title>
    <link rel="stylesheet" href="https://unpkg.com/reactflow@11.10.2/dist/style.css" />
    <style>
      html, body, #root {
        width: 100%;
        height: 100%;
        margin: 0;
        background-color: #f8f9fa;
        font-family: sans-serif;
      }
      .hazard { background:#ffcccc; border:2px solid #cc0000; }
      .barrier { background:#e6ffe6; border:2px solid #009900; }
      .threat  { background:#fff3cd; border:2px solid #ffcc00; }
      .consequence { background:#e0ecff; border:2px solid #0066cc; }
    </style>
  </head>
  <body>
    <div id="root"></div>

    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/reactflow@11.10.2/dist/reactflow.min.js"></script>

    <script type="text/javascript">
      const { ReactFlow, Background, Controls, MiniMap, useNodesState, useEdgesState, addEdge } = window.ReactFlow;

      const initialNodes = [
        { id: 'hazard', position: { x: 400, y: 200 }, data: { label: '⚠️ Hazard' }, className: 'hazard' },
        { id: 'threat1', position: { x: 150, y: 150 }, data: { label: 'Threat A' }, className: 'threat' },
        { id: 'barrier1', position: { x: 275, y: 150 }, data: { label: 'Barrier A' }, className: 'barrier' },
        { id: 'barrier2', position: { x: 525, y: 150 }, data: { label: 'Barrier B' }, className: 'barrier' },
        { id: 'cons1', position: { x: 650, y: 150 }, data: { label: 'Consequence A' }, className: 'consequence' },
      ];

      const initialEdges = [
        { id: 'e1', source: 'threat1', target: 'barrier1' },
        { id: 'e2', source: 'barrier1', target: 'hazard' },
        { id: 'e3', source: 'hazard', target: 'barrier2' },
        { id: 'e4', source: 'barrier2', target: 'cons1' },
      ];

      function Flow() {
        const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
        const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

        const onConnect = (params) => setEdges((eds) => addEdge(params, eds));

        return React.createElement(
          ReactFlow,
          {
            nodes,
            edges,
            onNodesChange,
            onEdgesChange,
            onConnect,
            fitView: true,
            attributionPosition: "bottom-left",
            style: { background: "#f8f9fa" }
          },
          React.createElement(Background, { variant: "dots" }),
          React.createElement(MiniMap, null),
          React.createElement(Controls, null)
        );
      }

      const root = ReactDOM.createRoot(document.getElementById('root'));
      root.render(React.createElement(Flow));
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=600, scrolling=False)
