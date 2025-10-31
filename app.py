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

# --- Initialize default graph ---
default_nodes = [
    {"id": "haz1", "type": "hazard", "data": {"label": "Hazard"}, "position": {"x": 0, "y": 0}},
    {"id": "top1", "type": "topevent", "data": {"label": "Top Event"}, "position": {"x": 0, "y": 200}},
]
default_edges = [{"id": "e1", "source": "haz1", "target": "top1"}]

if "nodes" not in st.session_state:
    st.session_state.nodes = default_nodes
if "edges" not in st.session_state:
    st.session_state.edges = default_edges

# --- Add new nodes logic ---
if add_button:
    nodes = st.session_state.nodes
    edges = st.session_state.edges
    new_id = f"n{len(nodes)+1}"
    label = label_input.strip() or node_type
    node = {"id": new_id, "type": node_type.lower().replace(" ", ""), "data": {"label": label}, "position": {"x": 0, "y": 0}}
    nodes.append(node)

    # Connect according to type
    if node_type == "Hazard":
        # Replace existing hazard
        nodes = [n for n in nodes if n["type"] != "hazard"]
        node["id"] = "haz1"
        nodes.insert(0, node)
        edges = [e for e in edges if e["source"] != "haz1" and e["target"] != "haz1"]
        edges.append({"id": "e_haz_top", "source": "haz1", "target": "top1"})

    elif node_type == "Top Event":
        node["id"] = "top1"
        nodes = [n for n in nodes if n["type"] != "topevent"]
        nodes.append(node)
        edges = [e for e in edges if e["source"] != "haz1" and e["target"] != "top1"]
        edges.append({"id": "e_haz_top", "source": "haz1", "target": "top1"})

    elif node_type in ["Threat", "Preventive Barrier"]:
        edges.append({"id": f"e{len(edges)+1}", "source": new_id, "target": "top1"})

    elif node_type in ["Mitigation Barrier", "Consequence"]:
        edges.append({"id": f"e{len(edges)+1}", "source": "top1", "target": new_id})

    st.session_state.nodes = nodes
    st.session_state.edges = edges

# --- Prepare JS data ---
nodes_js = str(st.session_state.nodes).replace("'", '"')
edges_js = str(st.session_state.edges).replace("'", '"')

# --- Render React Flow with Dagre Layout ---
html_code = f"""
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
      }}
      .react-flow__node-hazard {{
        border: 2px solid black;
        background: white;
        background-image: repeating-linear-gradient(
          45deg, #fff200, #fff200 10px, #000 10px, #000 20px
        );
        background-size: 100% 20px;
        color: #000;
        font-weight: bold;
        text-align: center;
      }}
      .react-flow__node-topevent {{
        background: #28a745;
        color: white;
        border: 3px solid #155724;
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

    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/reactflow@11.10.2/dist/reactflow.min.js"></script>
    <script crossorigin src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>

    <script>
      const {{ ReactFlow, Background, Controls, MiniMap }} = window.ReactFlow;

      const nodes = {nodes_js};
      const edges = {edges_js};

      // --- Dagre layout ---
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
            snapToGrid: true,
            proOptions: {{ hideAttribution: true }},
          }},
          React.createElement(Background, {{ variant: "dots" }}),
          React.createElement(Controls, null),
          React.createElement(MiniMap, null)
        );
      }}

      const root = ReactDOM.createRoot(document.getElementById("root"));
      root.render(React.createElement(App));
    </script>
  </body>
</html>
"""

st.components.v1.html(html_code, height=850, scrolling=False)
