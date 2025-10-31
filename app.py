import streamlit as st
st.set_page_config(page_title="Bowtie Risk Diagram (React Flow)", layout="wide")
st.title("🎯 Bowtie Risk Diagram – React Flow Auto Layout")

# --- Sidebar ---
st.sidebar.header("Add / Edit Elements")
node_type = st.sidebar.selectbox(
    "Select Node Type:",
    ["Hazard", "Top Event", "Threat", "Preventive Barrier", "Mitigation Barrier", "Consequence"],
)
label_input = st.sidebar.text_input("Label:", value=f"New {node_type}")
add_button = st.sidebar.button("➕ Add Node")

# --- Initialize nodes/edges ---
default_nodes = [
    {"id": "haz1", "type": "hazard", "data": {"label": "Hazard"}, "position": {"x": 0, "y": 0}},
    {"id": "top1", "type": "topevent", "data": {"label": "Top Event"}, "position": {"x": 0, "y": 200}},
]
default_edges = [{"id": "e1", "source": "haz1", "target": "top1"}]

if "nodes" not in st.session_state:
    st.session_state.nodes = default_nodes
if "edges" not in st.session_state:
    st.session_state.edges = default_edges

# --- Add node logic ---
if add_button:
    new_id = f"n{len(st.session_state.nodes)+1}"
    label = label_input.strip() or node_type
    node = {"id": new_id, "type": node_type.lower().replace(" ", ""), "data": {"label": label}, "position": {"x": 0, "y": 0}}
    st.session_state.nodes.append(node)

    if node_type == "Hazard":
        st.session_state.edges = [e for e in st.session_state.edges if e["source"] != "haz1"]
        st.session_state.edges.append({"id": f"e{len(st.session_state.edges)+1}", "source": "haz1", "target": "top1"})
    elif node_type in ["Threat", "Preventive Barrier"]:
        st.session_state.edges.append({"id": f"e{len(st.session_state.edges)+1}", "source": new_id, "target": "top1"})
    elif node_type in ["Mitigation Barrier", "Consequence"]:
        st.session_state.edges.append({"id": f"e{len(st.session_state.edges)+1}", "source": "top1", "target": new_id})

nodes_js = str(st.session_state.nodes).replace("'", '"')
edges_js = str(st.session_state.edges).replace("'", '"')

# --- HTML page for React Flow ---
react_html = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <title>Bowtie Diagram</title>
    <link rel="stylesheet" href="https://unpkg.com/reactflow@11.10.2/dist/style.css" />
    <style>
      html, body, #root {{
        width: 100%;
        height: 100%;
        margin: 0;
        background: #f8fafc;
        font-family: Arial, sans-serif;
      }}
      .react-flow__node-hazard {{
        border: 2px solid black;
        background: white;
        background-image: repeating-linear-gradient(
          45deg, #fff200, #fff200 10px, #000 10px, #000 20px
        );
        background-size: 100% 20px;
        color: #000;
        text-align: center;
        font-weight: bold;
      }}
      .react-flow__node-topevent {{
        background: #28a745;
        border: 3px solid #155724;
        color: white;
        text-align: center;
        font-weight: bold;
      }}
      .react-flow__node-threat {{
        background: #fff3cd;
        border: 2px solid #ffcc00;
        text-align: center;
      }}
      .react-flow__node-preventivebarrier,
      .react-flow__node-mitigationbarrier {{
        background: #cce5ff;
        border: 2px solid #007bff;
        text-align: center;
      }}
      .react-flow__node-consequence {{
        background: #f8d7da;
        border: 2px solid #dc3545;
        text-align: center;
      }}
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module">
      import React from "https://esm.sh/react@18.2.0";
      import ReactDOM from "https://esm.sh/react-dom@18.2.0";
      import ReactFlow, {{ Background, Controls, MiniMap }} from "https://esm.sh/reactflow@11.10.2";
      import dagre from "https://esm.sh/dagre@0.8.5";

      const nodes = {nodes_js};
      const edges = {edges_js};
      const dagreGraph = new dagre.graphlib.Graph();
      dagreGraph.setDefaultEdgeLabel(() => ({{}}));
      const nodeWidth = 180;
      const nodeHeight = 60;

      const layout = (nodes, edges) => {{
        dagreGraph.setGraph({{ rankdir: "TB", nodesep: 80, ranksep: 100 }});
        nodes.forEach(node => dagreGraph.setNode(node.id, {{ width: nodeWidth, height: nodeHeight }}));
        edges.forEach(edge => dagreGraph.setEdge(edge.source, edge.target));
        dagre.layout(dagreGraph);
        return nodes.map(node => {{
          const pos = dagreGraph.node(node.id);
          node.position = {{ x: pos.x - nodeWidth / 2, y: pos.y - nodeHeight / 2 }};
          return node;
        }});
      }};

      const layoutedNodes = layout(nodes, edges);

      function App() {{
        return React.createElement(
          ReactFlow,
          {{
            nodes: layoutedNodes,
            edges: edges.map(e => ({{
              ...e,
              markerEnd: {{ type: "arrowclosed", color: "#333" }},
              style: {{ stroke: "#333", strokeWidth: 2 }}
            }})),
            fitView: true,
            proOptions: {{ hideAttribution: true }}
          }},
          React.createElement(Background, {{ variant: "dots" }}),
          React.createElement(Controls, null),
          React.createElement(MiniMap, null)
        );
      }}

      ReactDOM.createRoot(document.getElementById("root")).render(React.createElement(App));
    </script>
  </body>
</html>
"""

# --- Render via iframe so it executes JS safely ---
st.components.v1.html(
    f'<iframe srcdoc="{react_html}" width="100%" height="850" style="border:none;"></iframe>',
    height=850,
    scrolling=False,
)

          
